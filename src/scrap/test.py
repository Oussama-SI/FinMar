import pyhdfs

# Connexion au NameNode via WebHDFS
# 9870 = port WebHDFS du NameNode exposé dans ton docker-compose
fs = pyhdfs.HdfsClient(hosts="localhost:9870", user_name="hdfs")

# Chemin du fichier à créer dans HDFS
path = "/user/hicham/mon_fichier2.txt"

# Contenu à écrire
contenu = """Bonjour Hadoop depuis Python !
Ce fichier a été créé avec WebHDFS et pyhdfs.
"""

# Création + écriture du fichier
fs.create(path, data=contenu.encode("utf-8"), overwrite=True)

# Vérification du contenu
print("✅ Fichier créé :", path)
print("📂 Contenu :")
print(fs.open(path).read().decode("utf-8"))
