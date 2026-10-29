@chapter Chapitre 7. Validations et perspectives

La validation constitue une étape essentielle du projet. Elle permet de vérifier la conformité des composants déployés avec les objectifs initiaux, ainsi que la stabilité et la fiabilité de l’environnement. Dans le cadre de cette étude, la validation a porté sur plusieurs volets : la mise en place du cluster Kubernetes, l’orchestration des microservices, la mise à l’échelle automatique, le fonctionnement du pipeline CI/CD et la communication entre les différents services.

## 7.1. Validation du cluster Kubernetes

La première phase de validation se concentre sur le bon fonctionnement du cluster Kubernetes. Celui-ci repose sur une architecture composée d’un nœud *master* et de deux nœuds *workers*, déployés à l’aide de Vagrant et VirtualBox. L’objectif est de confirmer la capacité du cluster à orchestrer et distribuer les conteneurs de manière dynamique, tout en assurant la haute disponibilité et la tolérance aux pannes.

L’exécution de la commande `kubectl get nodes` permet de vérifier que les trois nœuds apparaissent dans l’état `Ready`. L’option `-o wide` affiche en plus les adresses associées à chaque nœud du cluster (figure 30).

```
$ kubectl get nodes -o wide
```

@img fig_etude/p106_n131.png | 0.8 | État des nœuds du cluster Kubernetes

Une étape essentielle consiste à confirmer que le réseau de pods est fonctionnel et que la communication entre les différents nœuds se fait sans obstacle. Chaque pod doit pouvoir échanger avec tous les autres pods du cluster, même lorsqu’ils s’exécutent sur des nœuds distincts. Cette vérification passe par l’observation de l’état des pods du *namespace* `kube-system`, notamment ceux du réseau Calico (figure 31).

```
$ kubectl get pods -n kube-system
```

@img fig_etude/p107_n133.png | 0.8 | Pods système du cluster dans le namespace kube-system

Le plan de contrôle du cluster constitue également un élément critique à valider. Ses composants principaux, tels que le serveur d’API, l’ordonnanceur (*scheduler*) et le gestionnaire de contrôleurs (*controller manager*), doivent être actifs et capables de gérer la planification des pods et la répartition des ressources (figure 32).

```
$ kubectl get pods -n kube-system -l tier=control-plane
```

@img fig_etude/p107_n135.png | 0.8 | Composants du plan de contrôle

Le DNS interne du cluster, assuré par CoreDNS, est également vérifié. La résolution DNS permet aux services et aux pods de se localiser mutuellement (figure 33).

```
$ kubectl get pods -n kube-system -l k8s-app=kube-dns
```

@img fig_etude/p107_n137.png | 0.8 | Pods CoreDNS assurant la résolution DNS interne

Pour suivre l’utilisation des ressources et permettre la mise à l’échelle automatique des services, Kubernetes s’appuie sur le composant *Metrics Server* [15], déployé dans le *namespace* `kube-system`, qui collecte les données d’utilisation du CPU et de la mémoire de tous les nœuds et pods du cluster. Pour vérifier le bon fonctionnement des métriques, on exécute :

```
$ kubectl get pods -n kube-system | grep metrics-server
$ kubectl top nodes
$ kubectl top pods
```

La première commande permet de s’assurer que le pod `metrics-server` est dans l’état `Running`. Les deux suivantes affichent l’utilisation actuelle des ressources par les nœuds et les pods, confirmant que le cluster collecte correctement les métriques nécessaires au suivi et à la mise à l’échelle automatique (figure 34).

@img fig_etude/p108_n139.png | 0.8 | Collecte des métriques des nœuds et des pods

## 7.2. Validation des manifests des microservices

### 7.2.1. Notion de namespace

Dans Kubernetes, un *namespace* constitue un espace logique qui permet d’isoler et d’organiser les ressources au sein d’un même cluster. Chaque *namespace* peut contenir des pods, des services, des déploiements et d’autres objets Kubernetes. L’utilisation des *namespaces* facilite la gestion des ressources, la séparation des environnements (développement, test, production) et l’application de politiques spécifiques à un ensemble de services. Grâce à cette isolation, plusieurs équipes peuvent travailler simultanément dans le même cluster sans interférer entre elles.

La validation des microservices consiste à vérifier que chaque service déployé fonctionne correctement, communique avec les autres services et respecte les configurations prévues. On commence par lister les *namespaces* du cluster, parmi lesquels figure le *namespace* `microservices` (figure 35).

```
$ kubectl get namespace
```

@img fig_etude/p109_n141.png | 0.6 | Namespaces du cluster

### 7.2.2. Validation des pods et des services

La première étape de la validation des microservices consiste à vérifier l’état des pods dans le *namespace* dédié. Les pods représentent l’unité de base d’exécution dans Kubernetes et contiennent les conteneurs qui exécutent les microservices. Il est donc essentiel de s’assurer que chaque pod est correctement déployé et dans l’état `Running`, garantissant que les services associés peuvent fonctionner normalement.

```
$ kubectl get pods -n microservices
$ kubectl get pods -n microservices -o wide
```

La première commande fournit le nom, le statut, le nombre de redémarrages et l’âge de chaque pod. La seconde affiche en plus le nœud sur lequel chaque pod s’exécute et son adresse IP, facilitant la détection d’éventuels problèmes d’ordonnancement ou de répartition des pods sur les nœuds du cluster. La figure 36 montre que les pods des trois microservices sont en marche et répartis sur les deux nœuds *workers*.

@img fig_etude/p110_n143.png | 0.95 | Pods des microservices et leur répartition sur les nœuds

Une fois les pods validés, il est nécessaire de s’assurer que les *Services* Kubernetes fonctionnent correctement. Un *Service* agit comme une abstraction réseau permettant d’exposer un ensemble de pods via une adresse IP stable ; il assure le routage du trafic et la découverte automatique des pods, même lorsque ceux-ci sont recréés ou déplacés sur d’autres nœuds. La commande suivante affiche la liste des services, leur type, leurs ports et leurs adresses IP ; chaque service doit être correctement configuré et accessible dans le réseau interne du cluster (figure 37).

```
$ kubectl get svc -n microservices
```

@img fig_etude/p110_n145.png | 0.75 | Services ClusterIP des microservices

### 7.2.3. Validation de l’Ingress

Après la vérification des services internes, il est essentiel de valider la couche *Ingress*, qui permet d’exposer les microservices vers l’extérieur du cluster. L’*Ingress* agit comme un point d’entrée unique du trafic HTTP/HTTPS et redirige les requêtes vers les services internes selon les règles définies. Cette couche garantit un accès centralisé, sécurisé et contrôlé aux différentes API de l’application. Le manifest `microservices-ingress.yaml` s’appuie sur le contrôleur NGINX Ingress ; son bon fonctionnement est vérifié avec les commandes suivantes (figure 38) :

```
$ kubectl get pods -n ingress-nginx
$ kubectl get ingress -n microservices
```

@img fig_etude/p111_n147.png | 0.85 | Contrôleur NGINX Ingress et règles d’Ingress du namespace microservices

## 7.3. Validation de la mise à l’échelle automatique

La validation des *Horizontal Pod Autoscalers* et des métriques vise à s’assurer que le cluster est capable d’adapter automatiquement les ressources à la charge réelle des microservices. Cette étape garantit la scalabilité dynamique et la résilience du système.

Il est d’abord indispensable de confirmer que le *Metrics Server* est installé et opérationnel, puisque c’est lui qui collecte en continu les données d’utilisation du CPU et de la mémoire des pods :

```
$ kubectl get deployment metrics-server -n kube-system
$ kubectl top nodes
$ kubectl top pods -n microservices
```

Ces commandes doivent afficher la consommation de CPU et de mémoire de chaque nœud et de chaque pod ; si aucune donnée ne remonte, cela indique un problème de collecte des métriques (figure 39).

@img fig_etude/p111_n149.png | 0.85 | Metrics Server et consommation des ressources des microservices

Dans les résultats des commandes `kubectl top`, deux unités principales apparaissent :

- **CPU (m) :** le « m » signifie *millicores*. Kubernetes exprime la puissance de calcul en millièmes de cœur : 1000m correspond à un cœur complet, 500m à un demi-cœur et 1m à un millième de cœur. Cela permet une gestion très fine des ressources processeur attribuées à chaque pod ou conteneur.
- **Mémoire (Mi) :** le « Mi » signifie mébioctets (*mebibytes*). 1 Mi vaut 1 024 × 1 024 octets, soit environ 1,05 Mo. Kubernetes utilise cette unité binaire pour mesurer la mémoire avec plus de précision que les unités décimales classiques.

Une fois les métriques disponibles, la validation du mécanisme de mise à l’échelle automatique peut commencer. On liste les HPA du *namespace* des microservices ; chacun doit indiquer sa cible d’utilisation du CPU ainsi que le nombre actuel et les bornes de pods (figure 40).

```
$ kubectl get hpa -n microservices
```

@img fig_etude/p112_n151.png | 0.95 | Horizontal Pod Autoscalers des microservices au repos

Pour observer le comportement du HPA, on simule une charge sur un service donné, ici `auth-service`, en lançant un pod temporaire qui lui envoie des requêtes en continu :

```
$ kubectl run -i --tty load-generator --image=busybox -- /bin/sh
# while true; do wget -q -O- http://auth-service.microservices.svc.cluster.local:4001; done
```

Pendant la montée en charge, on surveille l’évolution automatique du nombre de pods :

```
$ kubectl get hpa -n microservices -w
$ kubectl get pods -n microservices
```

@img fig_etude/p113_n153.png | 0.95 | Réaction du HPA de auth-service à la montée en charge

@img fig_etude/p113_n155.png | 0.85 | Consommation des pods et création d’un nouveau pod de auth-service

Les figures 41 et 42 montrent que l’utilisation du CPU de `auth-service` dépasse le seuil de 70 % (jusqu’à 83 %) et qu’un troisième pod est alors créé automatiquement : le HPA réagit correctement à la charge. Une fois la charge arrêtée, le nombre de pods redescend progressivement au niveau initial, confirmant la capacité d’autorégulation du cluster. Ainsi, la validation des HPA et des métriques garantit que l’orchestration Kubernetes assure une allocation optimale des ressources, tout en maintenant les performances et la stabilité des microservices déployés.

## 7.4. Validation d’un déploiement de bout en bout

Pour valider le pipeline sur un changement réel d’un service, la procédure est la suivante :

- identifier la version actuelle des services ;
- effectuer un changement sur un service ;
- pousser les changements vers GitHub ;
- laisser GitHub Actions effectuer l’intégration de ce service spécifique ;
- laisser GitHub Actions déployer le service sur le cluster ;
- laisser Cypress lancer les tests automatiques après le déploiement.

La version actuelle des services est identifiée grâce à la requête `healthz` de chaque service, interrogée en continu à travers l’*Ingress* par le script suivant :

@code check.sh

La figure 43 montre que les trois services fonctionnent correctement sous la même version `v-3169`.

@img fig_etude/p114_n157.png | 0.85 | Réponses healthz des services avant le changement (version v-3169)

Un changement est ensuite apporté à la réponse `healthz` du service d’authentification, qui affichera trois points d’exclamation au lieu de deux. Il s’agit ici d’une modification volontairement mineure, mais le même processus s’applique à un changement majeur, comme l’ajout d’une nouvelle mutation ou d’un correctif.

```
// avant
healthz: {
  type: GraphQLString,
  resolve: () =>
    `Auth Service is healthy!! ${BUILD_DATE} #${VERSION}`,
},

// après
healthz: {
  type: GraphQLString,
  resolve: () =>
    `Auth Service is healthy!!! ${BUILD_DATE} #${VERSION}`,
},
```

Pour remonter ce changement, on effectue un *commit* avec le message « healthz update », puis un *push* vers le dépôt GitHub (figure 44).

@img fig_etude/p115_n161.png | 0.42 | Commit du changement depuis l’éditeur de code

Sur GitHub Actions, on retrouve facilement le *workflow* déclenché par ce *push* grâce au message du *commit* (figure 45). Chaque étape du *workflow* est accessible pour plus de détails en cliquant dessus.

@img fig_etude/p115_n163.png | 1.0 | Workflow déclenché par le push, en cours d’exécution

Le pipeline prend alors le relais pour effectuer l’intégration du service modifié. Seul `auth-service` ayant changé, seule son image est construite et poussée, avec la nouvelle version `v-2058` (figure 46). L’image est ensuite validée par la tâche de test, qui vérifie que le conteneur démarre correctement (figure 47).

@img fig_etude/p116_n165.png | 0.95 | Tâche build : construction de l’image de auth-service en version v-2058

@img fig_etude/p116_n167.png | 0.95 | Tâche test : validation du démarrage du conteneur

Une fois ces étapes validées, GitHub Actions déploie automatiquement le service sur le cluster Kubernetes : la nouvelle version est déployée progressivement, puis la disponibilité des pods est vérifiée à deux reprises avant de considérer le déploiement comme réussi (figure 48).

@img fig_etude/p117_n169.png | 0.95 | Tâche deploy : déploiement progressif et validation des pods

Enfin, pour garantir le bon fonctionnement après le déploiement, Cypress lance les tests automatiques de bout en bout. Ces tests vérifient que l’application fonctionne correctement, que les interactions entre les microservices sont maintenues et que les fonctionnalités répondent aux exigences attendues. Les quinze tests des cinq scénarios (panier, connexion, commandes, gestion des commandes et gestion des produits) sont passés avec succès (figure 49).

@img fig_etude/p117_n171.png | 0.95 | Tâche cypress : résultats des tests de bout en bout

Une fois le service déployé, la nouvelle version apparaît dans les vérifications, confirmant que le déploiement a été correctement appliqué et que le service fonctionne avec les modifications apportées : la version de `auth-service` devient `v-2058`, tandis que les autres services, non modifiés, restent en version `v-3169` (figure 50).

@img fig_etude/p118_n173.png | 0.85 | Réponses healthz après le déploiement (auth-service en version v-2058)

En cas de problème détecté lors des tests post-déploiement ou de dysfonctionnement en production, il est possible de procéder à un retour arrière, rétablissant rapidement la version stable précédente du service afin de garantir la continuité et la fiabilité de l’application. Durant tout le processus de déploiement d’une nouvelle version, la continuité des services est assurée par la gestion des pods et des réplicas dans le cluster Kubernetes : les anciennes instances continuent de répondre aux requêtes jusqu’à ce que les nouvelles soient opérationnelles et prêtes à prendre le relais.

En somme, l’ensemble du processus de déploiement met en évidence la scalabilité et la haute disponibilité offertes par l’architecture microservices orchestrée avec Kubernetes. Chaque service peut être déployé et mis à jour de manière indépendante, sans impacter les autres, ce qui garantit la continuité du fonctionnement. La gestion automatique des réplicas, la supervision des ressources et la possibilité de retour arrière assurent que les services restent fiables, performants et facilement évolutifs, tout en permettant des mises à jour rapides et sûres.

## 7.5. Perspectives d’amélioration

Les validations menées montrent que les objectifs du projet sont atteints. Plusieurs axes d’amélioration peuvent néanmoins être envisagés pour aller plus loin :

- **Supervision et alertes avancées :** mettre en place des métriques applicatives et des alertes permettant de surveiller en temps réel la santé des services et d’optimiser l’allocation des ressources ;
- **Pratiques DevSecOps :** intégrer au pipeline des contrôles de sécurité, comme l’analyse des vulnérabilités des images et des dépendances, afin de garantir la protection des données et des services face aux menaces potentielles ;
- **Traçabilité des versions :** remplacer l’option `--record`, désormais dépréciée par Kubernetes comme le signalent les journaux du pipeline, par un mécanisme d’annotation dédié pour l’historique des déploiements ;
- **Migration progressive de GESCOM :** appliquer cette démarche aux modules de l’application GESCOM (clients, articles, facturations), en les extrayant un à un du monolithe vers des microservices indépendants.

@front CONCLUSION GÉNÉRALE
@mode roman

La mise en œuvre de ce projet a permis d’illustrer l’importance de l’automatisation et de l’orchestration dans le développement moderne d’applications basées sur une architecture microservices. La conception d’un pipeline CI/CD a assuré l’intégration continue et la livraison rapide et fiable des services, tout en réduisant les risques d’erreurs liées aux interventions manuelles. L’utilisation de Docker pour la conteneurisation et de Kubernetes pour l’orchestration a favorisé la portabilité, la scalabilité et la haute disponibilité de l’ensemble des microservices, contribuant à une meilleure gestion des ressources et à une maintenance simplifiée.

Les tests automatisés intégrés au pipeline ont permis de valider le bon fonctionnement des services avant et après leur déploiement, garantissant la cohérence et la qualité des fonctionnalités mises en production. Le mécanisme de retour arrière automatique a par ailleurs démontré sa capacité à préserver la disponibilité d’un service lorsqu’une nouvelle version échoue. L’ensemble de ces pratiques a transformé le cycle de vie de l’application, le rendant plus modulaire, fiable et sûr.

En perspective, plusieurs axes d’amélioration peuvent être envisagés. L’implémentation de métriques et d’alertes avancées permettrait de surveiller en temps réel la santé des services et d’optimiser l’allocation des ressources. L’intégration de pratiques DevSecOps renforcerait la sécurité du pipeline, garantissant la protection des données et des services face aux menaces potentielles. Enfin, cette démarche pourrait être appliquée à la migration progressive des modules de l’application GESCOM vers des microservices.

Ainsi, ce projet constitue une base solide pour le déploiement et la gestion de systèmes modulaires modernes, et ouvre la voie à une amélioration continue des processus de développement et d’exploitation des applications en microservices.

@front BIBLIOGRAPHIE

= [1] NEWMAN Sam. *Building Microservices: Designing Fine-Grained Systems*. 2ᵉ édition. Sebastopol : O’Reilly Media, 2021.
@space 6
= [2] HUMBLE Jez, FARLEY David. *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*. Boston : Addison-Wesley, 2010.
@space 6
= [3] KIM Gene, HUMBLE Jez, DEBOIS Patrick, WILLIS John. *The DevOps Handbook*. Portland : IT Revolution Press, 2016.
@space 6
= [4] BURNS Brendan, BEDA Joe, HIGHTOWER Kelsey, EVENSON Lachlan. *Kubernetes: Up and Running*. 3ᵉ édition. Sebastopol : O’Reilly Media, 2022.
@space 6
= [5] CHACON Scott, STRAUB Ben. *Pro Git*. 2ᵉ édition. New York : Apress, 2014.

@front WEBOGRAPHIE

= [6] https://martinfowler.com/articles/microservices.html, *Microservices: a definition of this new architectural term*, FOWLER Martin, LEWIS James, consulté le 25/08/2025
@space 6
= [7] https://git-scm.com/doc, Documentation de Git, consulté le 01/09/2025
@space 6
= [8] https://docs.docker.com/, Documentation de Docker, consulté le 01/09/2025
@space 6
= [9] https://docs.github.com/actions, Documentation de GitHub Actions, consulté le 15/09/2025
@space 6
= [10] https://kubernetes.io/docs/, Documentation de Kubernetes, consulté le 15/09/2025
@space 6
= [11] https://developer.hashicorp.com/vagrant/docs, Documentation de Vagrant, consulté le 22/08/2025
@space 6
= [12] https://www.virtualbox.org/manual/, Manuel de VirtualBox, consulté le 22/08/2025
@space 6
= [13] https://docs.tigera.io/calico/latest/about/, Documentation de Calico, consulté le 25/08/2025
@space 6
= [14] https://kubernetes.github.io/ingress-nginx/, Documentation du contrôleur NGINX Ingress, consulté le 20/10/2025
@space 6
= [15] https://github.com/kubernetes-sigs/metrics-server, Documentation de Metrics Server, consulté le 20/10/2025
@space 6
= [16] https://graphql.org/learn/, Documentation de GraphQL, consulté le 06/10/2025
@space 6
= [17] https://docs.cypress.io/, Documentation de Cypress, consulté le 03/11/2025
@space 6
= [18] https://yaml.org/spec/1.2.2/, Spécification YAML 1.2.2, consulté le 15/09/2025

@front GLOSSAIRE

= **Calico :** plugin réseau (CNI) de Kubernetes qui assure la communication entre les pods répartis sur différents nœuds et l’application des politiques réseau.
@space 4
= **Cluster :** ensemble de machines (nœuds) gérées comme un tout par Kubernetes pour exécuter des applications conteneurisées.
@space 4
= **Conteneur :** environnement d’exécution isolé et léger qui embarque une application avec toutes ses dépendances.
@space 4
= **Deployment :** ressource Kubernetes décrivant l’état souhaité d’une application (image, nombre de réplicas) et gérant ses mises à jour progressives.
@space 4
= **GraphQL :** langage de requête pour API permettant au client de demander précisément les données dont il a besoin.
@space 4
= **Healthz :** point de contrôle de santé exposé par un service pour indiquer qu’il fonctionne, ici avec sa version et sa date de construction.
@space 4
= **Horizontal Pod Autoscaler (HPA) :** ressource Kubernetes qui ajuste automatiquement le nombre de pods d’un déploiement selon des métriques observées.
@space 4
= **Hotfix :** correctif urgent appliqué directement sur la version en production.
@space 4
= **Image Docker :** modèle immuable à partir duquel des conteneurs sont créés ; elle contient le code, l’environnement d’exécution et les dépendances.
@space 4
= **Ingress :** ressource Kubernetes qui expose des services HTTP/HTTPS vers l’extérieur du cluster et en définit les règles de routage.
@space 4
= **Job (tâche) :** ensemble d’étapes d’un workflow exécutées sur un même runner.
@space 4
= **Manifest :** fichier, généralement en YAML, décrivant de manière déclarative une ressource Kubernetes.
@space 4
= **Microservice :** service autonome, responsable d’une fonctionnalité métier précise, déployable indépendamment des autres.
@space 4
= **Monolithe :** application dont toutes les fonctionnalités sont regroupées dans un seul bloc déployé d’un seul tenant.
@space 4
= **Namespace :** espace logique isolant un ensemble de ressources au sein d’un cluster Kubernetes.
@space 4
= **Nœud (node) :** machine physique ou virtuelle faisant partie d’un cluster Kubernetes ; le nœud master héberge le plan de contrôle, les workers exécutent les pods.
@space 4
= **Orchestration :** automatisation du déploiement, de la mise à l’échelle, de la mise en réseau et de la supervision des conteneurs.
@space 4
= **Pipeline :** enchaînement automatisé des étapes de construction, de test et de déploiement d’une application.
@space 4
= **Pod :** plus petite unité déployable dans Kubernetes, regroupant un ou plusieurs conteneurs partageant le réseau et le stockage.
@space 4
= **Registre de conteneurs :** service de stockage et de distribution d’images Docker, ici le GitHub Container Registry.
@space 4
= **Réplica :** instance identique d’un pod ; plusieurs réplicas assurent la disponibilité et la répartition de la charge.
@space 4
= **Rollback (retour arrière) :** rétablissement de la version précédente d’une application après l’échec d’une mise à jour.
@space 4
= **Rolling update :** stratégie de mise à jour qui remplace progressivement les anciennes instances par les nouvelles, sans interruption de service.
@space 4
= **Runner :** agent qui exécute les tâches d’un workflow GitHub Actions ; il peut être hébergé par GitHub ou auto-hébergé.
@space 4
= **Service (Kubernetes) :** ressource offrant un point d’accès réseau stable à un ensemble de pods.
@space 4
= **Test de bout en bout (E2E) :** test qui vérifie le fonctionnement d’une application du point de vue de l’utilisateur, à travers l’ensemble de ses composants.
@space 4
= **Workflow :** processus automatisé défini dans un fichier YAML et déclenché par un événement du dépôt (push, pull request…).

@front TABLE DES MATIÈRES
@tdm

@front RÉSUMÉ

Ce mémoire présente la conception et la mise en œuvre d’un pipeline d’intégration et de déploiement continus (CI/CD) et de l’orchestration d’une application reposant sur des services indépendants. Chaque service fonctionne de manière autonome, communique avec les autres services et est testé automatiquement à chaque déploiement, ce qui garantit la fiabilité et la cohérence des fonctionnalités mises en production. Les services sont conteneurisés avec Docker, orchestrés par Kubernetes sur un cluster provisionné avec Vagrant et VirtualBox, et livrés par un pipeline GitHub Actions doté d’un mécanisme de retour arrière automatique. L’approche adoptée améliore la rapidité des mises à jour, facilite la maintenance, assure la continuité des services et réduit les erreurs liées aux interventions manuelles. Cette étude illustre l’importance de l’automatisation et de l’orchestration pour optimiser le cycle de vie des applications modernes.

= **Mots-clés :** microservices, automatisation, conteneurisation, orchestration, CI/CD, Kubernetes, tests automatisés.

@space 30
@center **ABSTRACT**
@space 14

This thesis presents the design and implementation of a continuous integration and deployment (CI/CD) pipeline and of the orchestration of an application based on independent services. Each service operates autonomously, communicates with the other services and is automatically tested at every deployment, ensuring the reliability and consistency of the deployed features. The services are containerized with Docker, orchestrated by Kubernetes on a cluster provisioned with Vagrant and VirtualBox, and delivered by a GitHub Actions pipeline with an automatic rollback mechanism. This approach improves update speed, simplifies maintenance, ensures service continuity and reduces errors caused by manual interventions. The study highlights the importance of automation and orchestration in optimizing the lifecycle of modern applications.

= **Keywords:** microservices, automation, containerization, orchestration, CI/CD, Kubernetes, automated testing.
