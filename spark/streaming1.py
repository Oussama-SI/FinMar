from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col, lower, regexp_replace
from pyspark.sql.types import StringType
from py4j.protocol import Py4JJavaError
import logging

# =============================================
# Compteur de mots en streaming via Socket
# =============================================
# Instructions d'utilisation :
# 1. Démarrer le serveur socket :
#    - Linux/macOS : nc -lk 9999
#    - Windows : netcat ou ncat -lk 9999
# 2. Exécuter l'application Spark :
#    spark-submit streaming_wordcount.py
# 3. Saisir du texte dans le terminal du serveur socket

def configure_spark_session():
    """Configure et retourne la session Spark"""
    return (SparkSession.builder
            .appName("StreamingWordCountSocket")
            .config("spark.sql.shuffle.partitions", "4")  # Optimisé pour le streaming
            .config("spark.streaming.stopGracefullyOnShutdown", "true")
            .getOrCreate())

def create_streaming_source(spark, host="localhost", port=9999):
    """Crée la source de données streaming depuis un socket"""
    return (spark.readStream
            .format("socket")
            .option("host", host)
            .option("port", port)
            .load()
            .selectExpr("CAST(value AS STRING) AS raw_text"))

def process_text_data(stream_df):
    """Transforme les données texte en mots individuels"""
    # Nettoyage et traitement du texte
    processed_text = stream_df.select(
        lower(regexp_replace(col("raw_text"), r"[^\w\s]", "")).alias("cleaned_text")
    )
    
    # Séparation en mots et filtrage
    words = (processed_text
             .select(explode(split(col("cleaned_text"), r"\s+")).alias("word"))
             .where(col("word") != "")
             .where(length(col("word")) > 1))  # Ignorer les mots d'une seule lettre
    
    return words

def main():
    # Configuration Spark
    spark = configure_spark_session()
    spark.sparkContext.setLogLevel("WARN")
    
    logger = logging.getLogger("py4j")
    logger.setLevel(logging.ERROR)
    
    print("🚀 Démarrage de l'application Spark Streaming WordCount...")
    print("📡 En attente de données sur le socket...")
    
    try:
        # === SOURCE : Lecture du flux socket ===
        source_stream = create_streaming_source(
            spark, 
            host="host.docker.internal",  # Adapter selon l'environnement
            port=9999
        )
        
        # === TRANSFORMATION : Traitement des mots ===
        words_stream = process_text_data(source_stream)
        
        # === AGRÉGATION : Comptage des mots ===
        word_counts = words_stream.groupBy("word").count()
        
        # === SINK : Écriture des résultats ===
        streaming_query = (word_counts.writeStream
                          .outputMode("update")          # Mode incrémental
                          .format("console")
                          .option("truncate", False)     # Affichage complet
                          .option("numRows", 10)         # Limite d'affichage
                          .trigger(processingTime="2 seconds")  # Intervalle de traitement
                          .start())
        
        # === GESTION DU CYCLE DE VIE ===
        print("✅ Application démarrée. Appuyez sur Ctrl+C pour arrêter.")
        streaming_query.awaitTermination()
        
    except KeyboardInterrupt:
        print("\n⏹️  Arrêt demandé par l'utilisateur...")
    except Py4JJavaError as e:
        print(f"❌ Erreur Spark détectée : {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
    finally:
        # === ARRÊT PROPRE ===
        print("🧹 Nettoyage des ressources...")
        for active_query in spark.streams.active:
            active_query.stop()
        spark.stop()
        print("✅ Application Spark arrêtée correctement.")

# Import supplémentaire pour la fonction length
from pyspark.sql.functions import length

if __name__ == "__main__":
    main()
