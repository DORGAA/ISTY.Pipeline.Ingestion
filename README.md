# ISTY.Pipeline.Ingestion


![github-small](https://i.ibb.co/xfXkCfZ/AWS-Pipeline-Infra.png)



# STACK INFORMATION 

Le projet consiste à la création d’une solution Serveless sur AWS permettant l’ingestion des données en temps réel. L’ingestion regroupe les phases de recueil et d’importation des données pour utilisation immédiate ou stockage dans une base. Le long de ses phases les données s’acheminent en continu ou s’ingèrent par lots.
Un front permettant la consultation des données sauvegardées et leurs gestions ( Opérations CRUD )

# Objectif  

* Prise en main de la console AWS
* Prise en main de l’infrastructure as code. ( Cloudformation SAM). de ressources et
permissions AWS
* Implémentation de la solution
* Monitoring et debuggage de la solution
* Automatisation du déploiement de la solution 
* Création d’un front Angular

# Iaas

L’infrastructure envisagée et présentée dans la figure précédente, est déployée en utilisant le framework aws officiel SAM, pour toute définition
concernant les ressources infrastructures à déployer est définie dans le fichier “template.yaml”. SAM utilise en effet le langage yaml de configuration, son syntaxe est une extension du syntaxe Cloudformation; le syntaxe natif de définition de ressources AWS.

# CI/CD

C’est la fusion entre deux groupes de pratiques, l’intégration continue et le déploiement continu. L’intégration continue consiste à abandonner l’intégration de
grands changements dans un projet partagé, pour le test et l’intégration de petits changements dans ce projet. L’intégration continue assure l’évolution du projet dans des petits incréments testés, validés et surtout fonctionnels. Le déploiement continu est un cycle automatique qui permet de monter et déployer la
totalité du projet lors de la détection d’un changement dans le code. L’approche CI/CD est automatique, et représente une solution aux contraintes d'intégration qui sont fréquemment rencontrées par les équipes de développement.

# Ressources AWS 

* AWS::S3::Bucket
* AWS::Serverless::Function
* AWS::DynamoDB::Table
* AWS::Serverless::Api 
