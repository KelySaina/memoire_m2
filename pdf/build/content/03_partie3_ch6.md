@part PARTIE III. MISE EN ŒUVRE

@chapter Chapitre 6. Installations et configurations

Cette partie présente la phase pratique du projet, où les concepts théoriques et les choix technologiques précédemment étudiés sont concrètement appliqués. Elle détaille la mise en place de l’infrastructure, la configuration des outils DevOps ainsi que le déploiement effectif d’une application conçue selon une architecture microservices. L’objectif est de démontrer comment l’automatisation du cycle de vie applicatif, de l’intégration au déploiement, peut améliorer la fiabilité, la rapidité et la cohérence des livrables.

L’application développée dans ce cadre est une application de commande de produits. Elle permet aux utilisateurs de consulter des produits et d’effectuer des commandes via une interface ou une API. Elle est découpée en trois services indépendants : la gestion des utilisateurs et de l’authentification, la gestion du catalogue de produits et la gestion des commandes, qui communiquent entre eux dans une architecture distribuée.

Ce choix d’application permet de mettre en pratique les principes fondamentaux du DevOps, notamment la conteneurisation, l’orchestration, l’intégration continue et le déploiement automatisé, tout en démontrant la flexibilité et la scalabilité offertes par une architecture découplée.

## 6.1. Infrastructure

Pour déployer et tester les microservices dans un environnement proche de la production, un cluster Kubernetes local composé d’un nœud *master* et de deux nœuds *workers* est utilisé. Ce cluster sert de base pour orchestrer les conteneurs, gérer la communication entre services et expérimenter les déploiements automatisés.

Pour mettre en place ce cluster, Vagrant est associé à VirtualBox. Vagrant permet d’automatiser la création, la configuration et le provisionnement de machines virtuelles, tandis que VirtualBox fournit la virtualisation nécessaire pour exécuter ces machines sur le poste hôte.

Le cluster est composé de trois nœuds : un *master* et deux *workers*, chacun disposant d’une adresse IP privée sur un réseau isolé. Le *master* orchestre le cluster et gère le plan de contrôle, tandis que les *workers* exécutent les conteneurs des microservices. Chaque machine virtuelle est configurée avec des ressources adaptées : le *master* dispose de 4 Go de RAM et de 2 vCPU, et les *workers* de 2 Go de RAM et d’1 vCPU chacun, garantissant une performance équilibrée pour un environnement local de test. Le fichier `Vagrantfile` utilisé est le suivant :

@code Vagrantfile

Le provisionnement des machines est entièrement automatisé via le script shell intégré dans le `Vagrantfile`. Ce script comprend plusieurs étapes :

- mise à jour du système d’exploitation (Ubuntu 20.04 LTS) et installation des prérequis, comme `curl` et les utilitaires réseau ;
- installation et configuration de Docker et de containerd, nécessaires pour exécuter les conteneurs ;
- installation des composants Kubernetes (`kubeadm`, `kubelet`, `kubectl`) et configuration des paramètres réseau permettant la communication entre nœuds et la gestion des pods ;
- mise à jour du fichier `/etc/hosts` sur chaque machine pour résoudre les noms de tous les nœuds, assurant une communication inter-nœuds fiable ;
- initialisation du *master* via `kubeadm init`, suivie de l’application d’un réseau de pods (Calico [13]) pour gérer le routage et la sécurité des communications ;
- connexion des *workers* au cluster via un script généré automatiquement par le *master* (`join.sh`), garantissant que les nœuds *workers* sont immédiatement opérationnels.

Cette approche permet de disposer d’un environnement Kubernetes complet et reproductible, où chaque machine est configurée de manière cohérente et où les microservices peuvent être déployés, testés et orchestrés de manière fiable. Grâce à Vagrant et VirtualBox, l’infrastructure peut être recréée rapidement sur n’importe quel poste de développement, facilitant la cohérence entre les équipes et la reproductibilité des tests. On obtient ensuite la topologie présentée dans la figure 10 : les trois nœuds sont placés dans un cluster Kubernetes avec Calico, qui permet aux pods de chaque nœud de communiquer entre eux même lorsqu’ils sont physiquement séparés.

@img fig_etude/p051_n013.png | 0.6 | Topologie du cluster Kubernetes

## 6.2. Automatisation CI/CD

Pour automatiser l’intégration et le déploiement des microservices, le projet utilise GitHub Actions avec des *runners* dédiés. Cette approche permet de déclencher automatiquement des *workflows* à chaque modification du code, garantissant la qualité, la cohérence et la réactivité des livraisons.

Dans un pipeline CI/CD, les *runners* GitHub jouent un rôle central : ce sont les agents chargés d’exécuter les *workflows* définis dans les fichiers YAML et d’enchaîner les différentes étapes du pipeline, de la compilation jusqu’au déploiement. Le tableau 19 présente les deux types de *runners* utilisés.

@tabcap Types de runners GitHub utilisés dans le projet
@colw 1,1,1.6,1.2,1.5
| Type de runner | Environnement | Avantages | Limites | Utilisation dans le projet |
|---|---|---|---|---|
| **Runners cloud (hébergés par GitHub)** | Serveurs GitHub | Maintenance minimale, ressources extensibles, exécution parallèle, rapides pour les *builds* et les tests | Ressources gratuites limitées, dépendance au cloud | Construction des images Docker, exécution des tests automatisés |
| **Runner auto-hébergé (*self-hosted*)** | Serveur local ou machine virtuelle | Contrôle total de l’environnement, accès direct au cluster, exécution des tâches nécessitant un accès au réseau interne | Nécessite une maintenance et une configuration manuelles | Déploiement des microservices sur le cluster Kubernetes local (*runner* du nœud *master*) |

### 6.2.1. Installation du runner

Dans l’architecture CI/CD du projet, les *runners* cloud sont utilisés pour construire et tester les microservices, ce qui permet de bénéficier d’une exécution rapide et parallèle sans surcharger l’infrastructure locale. Le *runner* auto-hébergé, installé sur le nœud *master* du cluster Kubernetes, prend en charge les déploiements, garantissant que les microservices sont mis à jour dans un environnement cohérent et proche de la production.

Le fonctionnement du pipeline est le suivant : lorsqu’un développeur effectue un *push* sur la branche principale, les tâches de construction et de test sont exécutées automatiquement sur les *runners* cloud. Une fois validées, le *runner* du nœud *master* applique les manifests Kubernetes pour déployer les services sur le cluster, assurant ainsi la mise à jour automatique des microservices. Cette configuration offre une séparation claire des responsabilités, optimise l’utilisation des ressources et garantit que chaque étape du pipeline est fiable, reproductible et traçable.

Pour configurer un agent sur le nœud *master* du cluster afin qu’il serve de *runner*, il est nécessaire de disposer d’un compte GitHub et d’un accès administrateur sur le nœud. Il faut ensuite se rendre dans le dépôt GitHub concerné, puis accéder à **Settings → Actions → Runners**, comme le montre la figure 11.

@img fig_etude/p053_n015.png | 1.0 | Accès aux paramètres des runners du dépôt GitHub

À partir de cette section, on choisit d’ajouter un nouveau *runner* et on sélectionne le système d’exploitation de la machine cible, ici Linux x64. GitHub fournit alors les commandes d’installation et d’enregistrement à exécuter sur le nœud *master* (figure 12).

@img fig_etude/p054_n017_redacted.png | 0.95 | Instructions d’installation d’un runner auto-hébergé

Sur le nœud *master*, on commence par créer un dossier dédié au *runner*, puis on y télécharge et décompresse la dernière version du paquet fourni par GitHub :

```
master@k8s-master $ mkdir actions-runner && cd actions-runner
master@k8s-master $ curl -o actions-runner-linux-x64-2.329.0.tar.gz -L \
    https://github.com/actions/runner/releases/download/v2.329.0/actions-runner-linux-x64-2.329.0.tar.gz
master@k8s-master $ tar xzf ./actions-runner-linux-x64-2.329.0.tar.gz
```

On lance ensuite le processus de configuration en liant le *runner* au dépôt GitHub grâce au jeton d’enregistrement temporaire fourni par GitHub (masqué ci-dessous) :

```
master@k8s-master $ ./config.sh --url https://github.com/KelySaina/microservices-project --token <TOKEN>
```

Le script affiche d’abord un message d’accueil, puis vérifie la connexion réseau vers GitHub et les permissions nécessaires, et crée les répertoires de travail destinés aux tâches et aux fichiers temporaires. On choisit ensuite le groupe et le nom du *runner*, qui servira à l’identifier dans l’interface GitHub, ainsi que des étiquettes (*labels*) facultatives permettant de diriger certaines tâches uniquement vers ce *runner* (figure 13).

@img fig_etude/p056_n023.png | 0.95 | Enregistrement du runner auprès du dépôt GitHub

Après la saisie de ces informations, le script copie les fichiers nécessaires dans le répertoire local, génère les scripts d’exécution et confirme que le *runner* est enregistré et que ses paramètres de travail sont sauvegardés (figure 14).

@img fig_etude/p056_n025.png | 0.95 | Configuration du dossier de travail du runner

Une fois la configuration terminée, on démarre le *runner* avec la commande `./run.sh`. Le terminal affiche alors en temps réel que le *runner* est connecté et en attente de tâches (figure 15).

@img fig_etude/p057_n027.png | 0.75 | Runner démarré et en attente de tâches

Chaque fois qu’un *workflow* GitHub Actions correspondant aux étiquettes configurées est déclenché, le *runner* récupère automatiquement la tâche, télécharge le code, exécute les étapes définies (construction, tests, déploiement) et renvoie les résultats à GitHub. Les figures 16 et 17 illustrent deux scénarios possibles : une tâche qui se termine avec succès, et une tâche dont une étape échoue, auquel cas le terminal signale l’erreur et la tâche est marquée en échec.

@img fig_etude/p057_n029.png | 0.75 | Exemple d’exécution d’une tâche réussie par le runner

@img fig_etude/p058_n031.png | 0.75 | Exemple d’exécution d’une tâche en échec

### 6.2.2. Configuration du pipeline

Le pipeline CI/CD est l’élément central qui automatise la construction, les tests et le déploiement des microservices. Pour ce projet, il est défini avec GitHub Actions dans un fichier YAML qui décrit les différentes étapes à exécuter lorsqu’un événement déclencheur se produit. Ce fichier, `ci.yml`, est placé dans le répertoire `.github/workflows/` du projet (figure 18).

@img fig_etude/p058_n033.png | 0.5 | Emplacement du fichier de workflow dans le dépôt

Le *workflow* est déclenché automatiquement à chaque *push* sur la branche `main`. Il définit des variables d’environnement globales qui centralisent les paramètres réutilisables : le registre de conteneurs, le propriétaire des images, le *namespace* Kubernetes et le délai d’attente de santé des pods.

@code ci.yml 1-12

Le pipeline est structuré en quatre tâches (*jobs*) : `build`, `test`, `deploy` et `cypress`, orchestrées avec des dépendances explicites (`needs`) pour garantir que les étapes critiques s’exécutent dans le bon ordre.

#### a) Tâche build

La tâche `build` s’exécute sur un *runner* GitHub standard (`ubuntu-latest`). Elle récupère le code du dépôt, puis se connecte au GitHub Container Registry pour pouvoir y pousser les images Docker. Une version globale est générée pour chaque exécution ; elle sert d’étiquette (*tag*) aux images Docker et est transmise aux tâches suivantes. Le pipeline détermine ensuite les services modifiés depuis le dernier *commit* en filtrant les dossiers `services/` du dépôt, ce qui permet de construire et de pousser uniquement les images concernées, économisant ainsi du temps et des ressources. Chaque image est étiquetée à la fois avec la version générée et avec `latest`.

@code ci.yml 13-76

#### b) Tâche test

La tâche `test` s’exécute après la construction, également sur un *runner* GitHub standard. Elle récupère les images Docker construites pour les services modifiés, puis valide chacune d’elles : le conteneur est démarré, le pipeline vérifie qu’il est toujours en cours d’exécution après quelques secondes et, si le service expose un port, il interroge son point d’accès `/graphql`. Un conteneur qui ne démarre pas ou s’arrête immédiatement fait échouer la tâche, ce qui bloque le déploiement.

@code ci.yml 77-139

#### c) Tâche deploy

La tâche `deploy` s’exécute sur le *runner* auto-hébergé, c’est-à-dire sur le nœud *master* du cluster Kubernetes. Elle vérifie d’abord la configuration de `kubectl` pour s’assurer de la connectivité avec le cluster. Le pipeline applique ensuite les manifests Kubernetes de base : il crée le *namespace* et déploie les services ainsi que les *Horizontal Pod Autoscalers* (HPA). Pour chaque service modifié, il met à jour l’image avec l’étiquette générée et ajoute une annotation de version pour assurer la traçabilité.

@code ci.yml 140-181

Un aspect clé de ce pipeline est la validation stricte de l’état des pods après le déploiement. Le pipeline attend que le déploiement soit terminé, puis vérifie que tous les pods sont prêts et effectue une seconde vérification après un court délai pour s’assurer que la mise à jour est stable. En cas de problème, il tente un retour arrière « intelligent » vers l’image précédente non étiquetée `latest`, garantissant que le service reste disponible et fonctionnel. Un délai maximal est également configuré pour éviter les blocages prolongés, et tout incident fait échouer la tâche afin d’être immédiatement signalé.

@code ci.yml 182-273

#### d) Tâche cypress

Enfin, la tâche `cypress` s’exécute après un déploiement réussi, sur le *runner* auto-hébergé. Elle installe les dépendances de l’interface web, démarre celle-ci, puis lance la suite de tests de bout en bout Cypress [17], qui simule les parcours des utilisateurs (connexion, panier, commandes, administration des produits et des commandes) sur la nouvelle version déployée. Les captures produites en cas d’échec sont conservées comme artefacts du *workflow*.

@code ci.yml 274-307

Ainsi, ce pipeline assure une automatisation complète et fiable, avec une livraison rapide des microservices, une gestion fine des versions et un mécanisme robuste de retour arrière en cas de défaillance. Chaque étape est traçable, de la détection des changements dans le dépôt jusqu’à la mise à jour des services dans le cluster Kubernetes et leur validation fonctionnelle, garantissant la cohérence et la sécurité du déploiement.

## 6.3. Configuration de l’orchestration : manifests Kubernetes

Pour orchestrer les microservices dans le cluster Kubernetes, on utilise des manifests Kubernetes au format YAML [10]. Ces fichiers décrivent de manière déclarative les ressources nécessaires à l’exécution et à la gestion des services, garantissant une orchestration reproductible et cohérente.

Chaque microservice possède son propre *Deployment*, qui définit le nombre de réplicas, l’image Docker à utiliser, les étiquettes, les ports exposés et la stratégie de mise à jour. Cela permet au cluster de gérer automatiquement le déploiement, la mise à l’échelle et la disponibilité des applications. Les *Services* Kubernetes associés exposent les microservices à l’intérieur du cluster et peuvent être de type ClusterIP, NodePort ou LoadBalancer selon les besoins.

Pour les microservices critiques, des *Horizontal Pod Autoscalers* (HPA) sont définis afin d’adapter dynamiquement le nombre de pods en fonction de métriques telles que l’utilisation du CPU. Cette approche garantit que les services peuvent supporter des variations de charge sans intervention manuelle.

Les manifests incluent également la configuration d’un *namespace*, permettant d’isoler les microservices dans un environnement spécifique et de faciliter la gestion des ressources et des accès :

@code namespace.yaml

Chaque déploiement est annoté avec sa version afin d’assurer une traçabilité complète et de faciliter les retours arrière en cas de problème. En pratique, le pipeline CI/CD applique ces manifests à chaque déploiement via la commande `kubectl apply`, ce qui met à jour les ressources et déclenche un déploiement progressif (*rollout*) automatique des services modifiés. Les étapes de validation vérifient ensuite que tous les pods sont prêts et fonctionnels.

### 6.3.1. Déploiements

Dans Kubernetes, un *Deployment* est une ressource qui décrit comment déployer une application, gérer ses réplicas et effectuer des mises à jour progressives. Il fournit une abstraction de gestion des pods, permettant à Kubernetes de s’occuper de la mise à l’échelle, de la mise à jour des images et du rétablissement en cas de défaillance. Chaque *Deployment* est associé à un sélecteur (*selector*) qui définit les pods ciblés grâce à des étiquettes. Cela garantit que les modifications apportées au *Deployment* (comme le changement d’image Docker) sont appliquées uniquement aux pods correspondants.

Les *Services* Kubernetes complètent les *Deployments* en fournissant un point d’accès stable aux pods, indépendamment de leur adresse IP dynamique. Un *Service* agit comme une couche d’abstraction réseau et peut être de différents types :

- **ClusterIP :** le type par défaut, qui expose le service uniquement à l’intérieur du cluster. Il convient aux microservices internes de ce projet, qui s’appellent mutuellement sans être directement accessibles depuis l’extérieur ;
- **NodePort :** expose le service sur un port spécifique de chaque nœud du cluster, permettant un accès externe limité ;
- **LoadBalancer :** utilisé dans des environnements cloud, il crée automatiquement un équilibreur de charge pour exposer le service à Internet ;
- **ExternalName :** associe le service à un nom DNS externe, redirigeant le trafic vers un service externe.

Le tableau 20 résume le rôle de ces deux ressources dans le projet.

@tabcap Rôle des ressources Deployment et Service dans le projet
@colw 1,2,2
| Ressource (*kind*) | Objectif principal | Usage dans le projet |
|---|---|---|
| **Deployment** | Gestion des pods, mise à l’échelle, mise à jour et retour arrière | Chaque microservice dispose d’un *Deployment* pour gérer ses pods |
| **Service** | Fournir un point d’accès stable et interne aux pods via des étiquettes | Expose les pods de chaque microservice avec un *Service* ClusterIP |

Les manifests des services sont regroupés dans le dossier `k8s/svcs` (figure 19).

@img fig_etude/p067_n047.png | 0.45 | Manifests des déploiements des microservices

Chaque microservice possède un *Deployment* et un *Service* de type ClusterIP, correspondant à une architecture de microservices interne et isolée du trafic externe. Les *Deployments* utilisent `replicas: 2`, garantissant une disponibilité minimale en cas de défaillance d’un pod. L’attribut `imagePullPolicy: Always` force le cluster à récupérer systématiquement l’image depuis le registre, ce qui est essentiel dans le cadre d’un pipeline CI/CD avec des mises à jour fréquentes. Chaque *Deployment* référence également `imagePullSecrets`, permettant l’authentification auprès du GitHub Container Registry et sécurisant le téléchargement des images privées. Le manifest du service d’authentification est le suivant :

@code auth-deployment.yaml

Les manifests des services de gestion des commandes et des produits suivent la même structure :

@code order-deployment.yaml

@code product-deployment.yaml

Prenons l’exemple du manifest de `order-service`. Le *Deployment* définit la manière dont le service est exécuté dans le cluster : il crée deux réplicas du conteneur `order-service`, garantissant la disponibilité même si un pod tombe en panne. Chaque pod exécute l’image Docker `ghcr.io/kelysaina/order-service` et expose le port 4002, ce qui permet aux autres composants du cluster de communiquer avec lui. Le champ `imagePullSecrets` autorise Kubernetes à accéder au registre privé pour récupérer l’image, et le sélecteur basé sur l’étiquette `app: order-service` permet au *Deployment* de gérer exactement les pods correspondants.

Le *Service* associé expose le *Deployment* à l’intérieur du cluster via une adresse ClusterIP stable, que les autres microservices peuvent utiliser pour communiquer avec `order-service`. Il redirige le trafic interne reçu sur le port 4002 vers les pods correspondants. Cette configuration permet à `order-service` de fonctionner de manière fiable et scalable, tout en restant accessible uniquement depuis l’intérieur du cluster, conformément à une architecture de microservices isolée et sécurisée.

### 6.3.2. Ingress

Un *Ingress* est une ressource Kubernetes qui fournit une méthode pour exposer des services du cluster vers l’extérieur via HTTP et HTTPS. Contrairement aux *Services* de type NodePort ou LoadBalancer, l’*Ingress* centralise la gestion de l’accès externe, le routage et les règles de sécurité, offrant une solution plus flexible et évolutive pour la distribution du trafic.

L’*Ingress* fonctionne avec un contrôleur (*Ingress Controller*) qui applique les règles définies dans les manifests [14]. Ces règles déterminent comment router les requêtes vers les différents services du cluster en fonction du chemin (`/auth`, `/orders`…) ou du nom d’hôte. Cela permet de regrouper plusieurs services derrière un seul point d’entrée, simplifiant la gestion des accès externes et réduisant le nombre d’équilibreurs de charge nécessaires. Dans un contexte de microservices, l’*Ingress* est particulièrement utile pour :

- exposer plusieurs services via un seul point d’entrée, évitant la multiplication des adresses IP externes ;
- router le trafic selon les chemins ou les sous-domaines, permettant à chaque microservice de recevoir uniquement le trafic qui lui est destiné ;
- s’intégrer aux outils CI/CD, facilitant les mises à jour automatiques et le déploiement continu de services accessibles depuis l’extérieur.

L’*Ingress* sert donc de passerelle d’accès contrôlée et centralisée pour tous les services exposés du cluster. Le manifest utilisé est le suivant :

@code microservices-ingress.yaml

Ce manifest configure un *Ingress* centralisant l’accès externe aux trois microservices : `auth-service`, `order-service` et `product-service`. La version d’API `networking.k8s.io/v1` correspond à la version stable de l’API de gestion des *Ingress*, et le type `Ingress` définit la ressource comme un point d’entrée HTTP/HTTPS pour router le trafic externe vers les services internes.

Dans la section `metadata`, le nom identifie l’*Ingress* (`microservices-ingress`) et le *namespace* précise que cette configuration s’applique au *namespace* `microservices`. Les annotations configurent le comportement du contrôleur NGINX :

- `kubernetes.io/ingress.class: nginx` indique que cet *Ingress* doit être géré par un contrôleur NGINX ;
- `nginx.ingress.kubernetes.io/use-regex: "true"` permet l’utilisation d’expressions régulières dans les chemins ;
- `nginx.ingress.kubernetes.io/rewrite-target: /graphql` réécrit le chemin d’accès vers `/graphql` au niveau du service cible.

La section `spec` contient les règles de routage. Le champ `host: myapp.local` définit le domaine utilisé pour accéder aux services, et chaque service est associé à un chemin spécifique :

- `/auth(/|$)` redirige le trafic vers `auth-service` sur le port 4001 ;
- `/orders(/|$)` redirige vers `order-service` sur le port 4002 ;
- `/products(/|$)` redirige vers `product-service` sur le port 4003.

Le type de chemin `ImplementationSpecific` laisse au contrôleur NGINX le soin d’interpréter le routage selon sa logique interne. Dans le contexte du projet, cet *Ingress* offre un point d’accès unique pour tous les microservices via le domaine `myapp.local`, un routage flexible basé sur les chemins qui isole les services tout en conservant un accès centralisé, une réécriture de chemin qui simplifie les requêtes côté client, ainsi qu’une grande facilité d’évolution : de nouveaux services peuvent être ajoutés simplement en créant de nouvelles règles.

### 6.3.3. Horizontal Pod Autoscalers

Le *Horizontal Pod Autoscaler* (HPA) est une ressource Kubernetes qui ajuste automatiquement le nombre de pods d’un *Deployment*, d’un *ReplicaSet* ou d’un *StatefulSet* en fonction de métriques observées, telles que l’utilisation du CPU, de la mémoire ou de métriques personnalisées. L’objectif est d’assurer que l’application reste performante face aux variations de charge tout en optimisant l’usage des ressources.

Le HPA surveille en continu les métriques d’utilisation des pods et ajuste horizontalement leur nombre (augmentation ou diminution) pour répondre à la demande. Contrairement à une mise à l’échelle manuelle, il réagit automatiquement et en temps réel aux pics de trafic comme aux périodes de faible utilisation. Dans un contexte de microservices, le HPA est particulièrement utile pour :

- maintenir la disponibilité et la réactivité des services critiques sous forte charge ;
- optimiser l’utilisation des ressources du cluster en réduisant le nombre de pods lorsque la demande diminue ;
- soutenir la scalabilité automatique, essentielle lorsque la charge varie d’un service à l’autre ;
- permettre aux nouvelles versions déployées par le pipeline CI/CD de bénéficier immédiatement d’une mise à l’échelle automatique.

La mise en place d’un HPA commence par l’identification du *Deployment* cible auquel la mise à l’échelle automatique doit s’appliquer. Il faut ensuite définir les bornes de mise à l’échelle, c’est-à-dire le nombre minimal et maximal de pods : le service conserve ainsi une disponibilité minimale en période de faible charge, sans consommation excessive de ressources en période de forte demande. La configuration inclut enfin le choix des métriques à surveiller, le plus souvent l’utilisation du CPU et de la mémoire. Une fois déployé, le HPA est suivi pour s’assurer que la mise à l’échelle fonctionne correctement. Les manifests des HPA sont regroupés dans le dossier `k8s/hpas` (figure 20).

@img fig_etude/p075_n057.png | 0.45 | Manifests des Horizontal Pod Autoscalers

@code auth-hpa.yaml

@code order-hpa.yaml

@code product-hpa.yaml

Ces manifests présentent plusieurs points communs qui reflètent une approche cohérente de la mise à l’échelle automatique dans le projet. Tous ciblent un *Deployment* spécifique via `scaleTargetRef`, en précisant la version d’API, le type de ressource et le nom du microservice concerné. Chaque HPA définit un nombre minimal et maximal de pods pour encadrer la mise à l’échelle, garantissant à la fois la disponibilité minimale du service et une capacité maximale suffisante pour absorber la charge. La métrique utilisée est l’utilisation du CPU, avec un seuil cible (`averageUtilization`) de 70 à 75 %. Enfin, tous les HPA sont déployés dans le *namespace* `microservices`, ce qui centralise la gestion et facilite l’administration et la supervision.

En appliquant l’ensemble de ces manifests, on obtient dans Kubernetes l’architecture présentée dans la figure 21 :

- l’*Ingress* centralise l’accès HTTP et redirige vers les services selon les chemins définis (`/auth`, `/orders`, `/products`) ;
- chaque microservice possède un *Deployment* avec plusieurs réplicas pour la haute disponibilité ;
- les *Services* ClusterIP exposent les pods à l’intérieur du cluster pour la communication interne et pour l’*Ingress* ;
- les HPA ajustent dynamiquement le nombre de pods selon la charge CPU, assurant scalabilité et performance.

@img fig_etude/p079_n065.png | 0.85 | Architecture des microservices déployés dans Kubernetes

## 6.4. Application et services à déployer

Le projet repose sur une architecture microservices, chaque service ayant un rôle spécifique et autonome. Les services déployés sont présentés dans le tableau 21.

@tabcap Services de l’application déployée
@colw 1,1.1,2.8
| Service | Rôle principal | Description |
|---|---|---|
| **Service d’authentification (auth-service)** | Authentification et gestion des utilisateurs | Permet la création de comptes, l’authentification, la gestion des profils et des rôles (client, administrateur). |
| **Service des produits (product-service)** | Gestion des produits | Gère le catalogue des produits : ajout, mise à jour du stock et consultation des articles disponibles. |
| **Service des commandes (order-service)** | Gestion des commandes | Permet aux utilisateurs authentifiés de passer, consulter et suivre leurs commandes. Il communique avec le service des produits pour vérifier la disponibilité et avec le service d’authentification pour obtenir les informations des utilisateurs. |

Chaque service fonctionne de manière indépendante et communique via des requêtes GraphQL [16], ce qui assure la cohérence des données et la scalabilité du système. Cette architecture facilite le déploiement et la maintenance, tout en permettant l’évolution future du projet par l’ajout de nouveaux services ou de nouvelles fonctionnalités. Chaque service écrit également sa version et sa date de construction dans un fichier `version.json` lors de la construction de son image, et les expose via une requête `healthz` utilisée pour vérifier la version effectivement déployée.

### 6.4.1. Service d’authentification : Node.js / GraphQL / MySQL

Le service d’authentification est développé en Node.js avec GraphQL et utilise MySQL pour la persistance des données. Il est responsable de la création de comptes, de l’authentification des utilisateurs et de la gestion des rôles et des profils. Sa structure repose sur une organisation claire des fichiers, chacun ayant un rôle précis : gestion des utilisateurs, communication avec la base de données et exposition des fonctionnalités via l’API GraphQL (figure 22).

@img fig_etude/p081_n067.png | 0.5 | Structure du service d’authentification

Le fichier `db.js` contient la configuration de la connexion à la base de données MySQL. Il initialise un ensemble (*pool*) de connexions et l’exporte afin qu’il puisse être utilisé dans les autres modules du service.

@code auth.db.js

Le `Dockerfile` permet de construire l’image Docker du service. Il facilite le déploiement, assure l’isolation de l’environnement et garantit que le service s’exécute de manière identique sur différentes machines. Les arguments `VERSION` et `BUILD_DATE`, transmis par le pipeline, sont écrits dans le fichier `version.json` de l’image.

@code auth.Dockerfile

Le fichier `index.js` constitue le point d’entrée de l’application. Il initialise le serveur Node.js et GraphQL, configure les *middlewares* nécessaires et démarre l’écoute des requêtes entrantes.

@code auth.index.js

Le fichier `package.json` gère les dépendances du projet, notamment `express`, `graphql`, `bcryptjs`, `jsonwebtoken` et `mysql2`, et garantit que les versions utilisées sont cohérentes pour tous les développeurs et environnements.

@code auth.package.json

Enfin, le fichier `schema.js` définit le schéma GraphQL du service. Il décrit le type utilisateur, ainsi que les requêtes (`user`, `users`, `healthz`) et les mutations (`register`, `login`) disponibles. Les mots de passe sont hachés avec bcrypt et la connexion renvoie un jeton JWT valable 24 heures.

@code auth.schema.js

### 6.4.2. Service de gestion des produits : Python / GraphQL / MySQL

Le service de gestion des produits est développé en Python avec Flask et la bibliothèque GraphQL Ariadne, et utilise MySQL pour la persistance des données. Il est responsable de la création, de la mise à jour du stock et de la consultation des produits du catalogue. Sa structure est présentée dans la figure 23.

@img fig_etude/p087_n083.png | 0.5 | Structure du service de gestion des produits

Le fichier `db.py` contient la configuration de la connexion à la base de données MySQL et met à disposition un *pool* de connexions pour les autres modules.

@code product.db.py

Le `Dockerfile` permet de construire l’image Docker du service, facilitant le déploiement et l’isolation.

@code product.Dockerfile

Le fichier `app.py` constitue le point d’entrée de l’application. Il initialise le serveur Flask, active le CORS, expose l’interface de test GraphQL (requête GET) et l’API GraphQL (requête POST) sur le chemin `/graphql`, puis démarre l’écoute des requêtes sur le port 4003.

@code product.app.py

Le fichier `requirements.txt` liste les dépendances Python nécessaires au service, comme Flask, Ariadne, `graphql-core` et `mysql-connector-python`.

@code product.requirements.txt

Enfin, le fichier `schema.py` définit le schéma GraphQL du service. Il décrit le type produit, les requêtes de consultation du catalogue (`products`, `product`, `healthz`) et les mutations d’ajout de produit et de mise à jour du stock (`addProduct`, `updateStock`).

@code product.schema.py

### 6.4.3. Service de gestion des commandes : Node.js / GraphQL / MySQL

Le service de gestion des commandes est développé en Node.js avec GraphQL et utilise MySQL pour la persistance des données. Il est responsable de la création des commandes, de leur consultation et de la mise à jour de leur statut. Il communique avec le service des produits pour vérifier le prix et le stock disponibles, et avec le service d’authentification pour obtenir les informations des utilisateurs. Sa structure est présentée dans la figure 24.

@img fig_etude/p094_n099.png | 0.5 | Structure du service de gestion des commandes

Le fichier `db.js` contient la configuration de la connexion à la base de données MySQL et exporte le *pool* de connexions utilisé par les autres modules du service.

@code order.db.js

Le `Dockerfile` permet de construire l’image Docker du service de gestion des commandes, selon le même principe que pour les autres services.

@code order.Dockerfile

Le fichier `auth.js` fournit une fonction qui sécurise l’accès aux fonctionnalités du service. Elle extrait le jeton JWT de l’en-tête `Authorization` de la requête, le vérifie à l’aide de la clé secrète et retourne les informations de l’utilisateur si le jeton est valide.

@code order.auth.js

Le fichier `index.js` constitue le point d’entrée de l’application. Il initialise le serveur Node.js et GraphQL, injecte l’utilisateur authentifié dans le contexte de chaque requête et démarre l’écoute des requêtes entrantes sur le port 4002.

@code order.index.js

Le fichier `package.json` gère les dépendances du service ; on y retrouve notamment `axios`, utilisé pour interroger les autres microservices.

@code order.package.json

Enfin, le fichier `schema.js` définit le schéma GraphQL du service. Il décrit les types commande et ligne de commande, les requêtes (`myOrders`, `orders`, `healthz`) et les mutations (`createOrder`, `updateOrderStatus`). La création d’une commande interroge le service des produits pour chaque article, vérifie le stock, calcule le montant total et enregistre la commande et ses lignes dans une transaction, annulée en cas d’erreur. Les informations sur les produits et les utilisateurs d’une commande sont résolues à la demande auprès des services correspondants.

@code order.schema.js

## 6.5. Vérification des jobs

L’intégration et le déploiement de chaque microservice sont automatisés avec GitHub Actions. Cet outil permet de définir des *workflows* déclenchés par des événements sur le dépôt, comme un *push*, une *pull request* ou une planification horaire. Chaque *workflow* est composé de tâches (*jobs*), qui sont des séries d’étapes s’exécutant dans un environnement défini et qui peuvent inclure des tests, des constructions et des déploiements.

Pour accéder à l’interface de GitHub Actions, il faut se connecter à son compte GitHub, ouvrir le dépôt du projet, puis cliquer sur l’onglet **Actions** dans la barre supérieure. Cet onglet affiche la liste des *workflows* configurés dans le dépôt et de leurs exécutions (figure 25).

@img fig_etude/p103_n121.png | 1.0 | Onglet Actions du dépôt GitHub

En sélectionnant une exécution, il est possible de consulter son statut (réussie, en échec ou en cours) ainsi que l’enchaînement de ses tâches. Cette interface permet de suivre l’historique des exécutions et de vérifier la qualité et la fiabilité des tâches. Les figures 26 et 27 présentent respectivement une exécution réussie et une exécution en échec lors de la tâche de déploiement.

@img fig_etude/p103_n123.png | 1.0 | Exécution réussie du workflow CI/CD

@img fig_etude/p104_n125.png | 1.0 | Exécution du workflow en échec lors du déploiement

Pour une exécution donnée, il est possible d’ouvrir le détail des tâches et de leurs étapes. Chaque étape peut être inspectée individuellement pour vérifier qu’elle s’est exécutée correctement, consulter les journaux ou diagnostiquer les éventuelles erreurs (figure 28). Cette fonctionnalité est essentielle pour assurer la robustesse et la continuité des *workflows* d’intégration et de déploiement continus.

@img fig_etude/p104_n127.png | 0.6 | Détail des étapes d’une tâche de déploiement réussie

La figure 29 montre les journaux d’une tâche de déploiement en échec : le déploiement de `product-service` n’a pas abouti dans le délai imparti, et le pipeline a automatiquement rétabli l’image précédente du service (`v-2896`) avant de signaler l’échec. Le service est ainsi resté disponible malgré la défaillance de la nouvelle version.

@img fig_etude/p105_n129.png | 0.95 | Journaux d’un déploiement en échec suivi d’un retour arrière automatique
