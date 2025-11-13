from pyspark.sql import SparkSession

print("🔧 ÉTAPE 1 : PREMIER CONTACT AVEC SPARK")
print("=" * 50)

# 1. Création de la session Spark
spark = SparkSession.builder \
    .appName("PremierContact") \
    .getOrCreate()

spark.sparkContext.setLogLevel = "ERROR"

print("✅ Session Spark créée avec succès!")

# 2. Test de connexion à HDFS
try:
    df = spark.read.option("header", "true") \
        .csv("hdfs://namenode:9000/shared/ventes_detaillees.csv")
    
    print("✅ Connexion à HDFS réussie!")
    print(f"📊 Nombre de lignes chargées : {df.count()}")
    
    # 3. Aperçu des données
    print("\n👀 Aperçu des données :")
    df.show(5)
    
    # 4. Structure des données
    print("\n📋 Structure du dataset :")
    df.printSchema()
    
except Exception as e:
    print(f"❌ Erreur : {e}")

# 5. Nettoyage
spark.stop()
print("\n🎯 ÉTAPE 1 TERMINÉE - Prêt pour la suite!")
