@part PARTIE II. ANALYSE PRÉALABLE ET CHOIX DES OUTILS

@chapter Chapitre 4. Analyse de l’existant et problématique

Afin de définir une solution adaptée, il est nécessaire de comprendre le fonctionnement actuel de l’application concernée, son processus de déploiement, sa méthodologie de test ainsi que l’infrastructure sur laquelle elle repose.

## 4.1. Analyse de l’existant

### 4.1.1. Architecture logicielle : GESCOM

L’application GESCOM (Gestion commerciale) est actuellement développée sous forme monolithique, ce qui signifie qu’un seul bloc applicatif gère l’ensemble des fonctionnalités, sans séparation en modules indépendants. Elle est développée en PHP avec le framework CodeIgniter suivant le modèle MVC. L’application expose également des endpoints REST permettant une interaction avec d’autres systèmes, mais la structure monolithique limite la flexibilité de cette intégration. La figure 6 présente cette architecture.

@img fig_etude/p025_n004.png | 0.42 | Architecture logicielle actuelle de l’application GESCOM

La base de données associée à l’application est unique et contient plus de 200 tables. Ces tables sont fortement couplées aux différentes fonctionnalités de l’application, ce qui rend toute modification ou évolution complexe. Les relations multiples entre les tables augmentent la dépendance entre les modules et compliquent la maintenance.

Les fonctionnalités principales de l’application incluent la gestion des clients, la gestion des articles et la gestion des facturations. Ces modules sont intégrés dans le même monolithe, ce qui centralise toutes les opérations mais limite la modularité et la flexibilité pour faire évoluer l’application ou la mettre à l’échelle. Le tableau 10 synthétise les points forts et les limites de cette architecture.

@tabcap Points forts et limites de l’architecture actuelle de GESCOM
@colw 1,1
| Points forts | Limites / contraintes |
|---|---|
| Solution centralisée avec toutes les fonctionnalités dans la même application | Faible modularité : difficile de déployer ou de faire évoluer une seule fonctionnalité |
| Utilisation d’un framework connu et documenté (CodeIgniter) | Maintenance difficile en raison du couplage élevé et de la taille de la base de données |
| Les endpoints REST permettent une intégration externe | Scalabilité limitée : il est nécessaire de mettre à l’échelle l’ensemble du monolithe, et non seulement certains modules |
| | Testabilité réduite : difficile de tester les fonctionnalités de manière isolée |
| | Risque de régression élevé lors des modifications |
| | Évolutivité technologique limitée : migration vers des architectures modernes plus complexe |

### 4.1.2. Processus de déploiement

Le déploiement de l’application GESCOM se fait à partir d’un serveur de production sur lequel un hôte virtuel (VHOST) est configuré pour héberger l’application. L’environnement de développement est local, sur le poste du développeur, et suit le principe Git Flow. Chaque nouvelle fonctionnalité ou correction est développée dans une branche *feature*, testée localement, puis fusionnée dans la branche *develop*.

Une fois les fonctionnalités consolidées et validées, la branche *develop* fait l’objet d’une fusion et d’un *finish* pour créer une *release*, qui est ensuite fusionnée dans la branche *master*. Le serveur de production récupère ensuite la dernière version stable en effectuant un `git pull` sur la branche *master*. Après ce *pull*, l’application est immédiatement opérationnelle sur le serveur de production, grâce au VHOST déjà configuré. La figure 7 illustre ce processus.

@img fig_etude/p027_n006.png | 0.62 | Processus de déploiement actuel de GESCOM

Ce processus est simple et direct, mais présente certaines limites : il repose entièrement sur un déploiement manuel, la mise à jour du serveur de production est sensible aux erreurs humaines, et il n’existe pas de mécanisme automatique de retour arrière (*rollback*) en cas de problème. La scalabilité et la gestion simultanée de plusieurs environnements restent également limitées.

### 4.1.3. Méthodologie de test

La méthodologie de test appliquée dans le cadre de l’application GESCOM repose principalement sur des tests manuels effectués après chaque mise en production (MEP). À chaque nouveau déploiement, seules les nouvelles fonctionnalités introduites ou modifiées sont testées manuellement afin de vérifier leur bon fonctionnement dans l’environnement de production.

Les autres fonctionnalités existantes ne sont pas systématiquement retestées, sauf en cas de bug signalé ou d’anomalie constatée par les utilisateurs. Cette méthodologie présente les limites suivantes :

- absence de tests de non-régression sur les fonctionnalités existantes ;
- détection tardive des anomalies, souvent remontées par les utilisateurs eux-mêmes ;
- tests effectués directement en production, après la mise à disposition de la nouvelle version ;
- qualité des tests dépendante de la disponibilité et de la rigueur des personnes qui les réalisent ;
- absence de traçabilité des tests réalisés et de leurs résultats.

### 4.1.4. Gestion des régressions

Lorsqu’une défaillance est détectée après un déploiement, le problème est remonté à l’équipe de développement. Le correctif est ensuite appliqué localement, puis redéployé en production après validation.

En cas d’échec majeur ou d’instabilité après la mise en production, il est possible de revenir manuellement à la dernière version stable qui fonctionnait correctement. Cette restauration est suivie d’une nouvelle phase de correction et de test avant de relancer le déploiement. Dans certains cas urgents, une branche *hotfix* est créée pour corriger rapidement le problème directement sur la branche *master*, avant de propager les changements dans les autres branches Git.

Les limites de cette méthodologie sont les suivantes :

- processus de correction et de redéploiement lent et manuel ;
- risque d’erreur humaine lors du retour arrière ou du redéploiement ;
- gestion complexe des branches après un *hotfix* (risque de désynchronisation entre *master* et *develop*) ;
- aucune validation automatique des correctifs avant la mise en production ;
- possibilité d’introduire de nouveaux bugs par précipitation.

### 4.1.5. Topologie de l’infrastructure

#### a) Environnement de développement local

La topologie de l’infrastructure actuellement utilisée pour le développement de l’application GESCOM est très simple et repose sur un environnement local. Le développeur travaille depuis un ordinateur (PC de développement) sur lequel sont installés l’environnement PHP, le framework CodeIgniter et les outils nécessaires au développement.

Ce poste est connecté à un routeur qui assure l’accès à Internet, notamment pour le téléchargement des dépendances, la gestion du dépôt Git et la synchronisation des modifications avec le serveur distant. Les développements, tests unitaires et validations se font localement avant la mise à jour du dépôt Git. La figure 8 représente cet environnement.

@img fig_etude/p029_n008.png | 0.5 | Topologie de l’environnement de développement local

Les caractéristiques du poste de développement et du routeur sont présentées respectivement dans les tableaux 11 et 12.

@tabcap Caractéristiques du poste de développement
@colw 1,1.6
| Élément | Spécifications techniques |
|---|---|
| Type de poste | PC de développement |
| Marque / Modèle | Dell |
| Processeur (CPU) | Intel Core i5 9ᵉ génération – 2,90 GHz |
| Mémoire vive (RAM) | 8 Go |
| Système d’exploitation | Windows 10 |
| Connexion réseau | Routeur pour l’accès à Internet |

@tabcap Caractéristiques du routeur d’accès à Internet
@colw 1,1.6
| Catégorie | Détails |
|---|---|
| Modèle | Huawei B612-233 (Flybox 4G+) |
| Type de réseau | 4G LTE Catégorie 6 (descendant jusqu’à ~300 Mbit/s, montant jusqu’à ~50 Mbit/s) |
| Fréquences LTE supportées | Bandes 4G : B1/B3/B7/B8/B20/B38/B40/B41/B42/B43 selon la variante |
| Wi-Fi | Standard 802.11 b/g/n, bande 2,4 GHz, jusqu’à ~32 appareils connectés |
| Ports Ethernet | 4 × Gigabit RJ45 (3 LAN + 1 LAN/WAN) |
| Port téléphonique | 1 × RJ11 pour ligne fixe / VoIP selon le modèle |
| Emplacement SIM | Micro-SIM |
| Alimentation | DC 12 V / 1 A (AC 100-240 V via adaptateur) |
| Dimensions / Poids | Environ 155 mm × 240 mm × 78 mm / ~430 g (hors adaptateur) |

#### b) Topologie globale et serveurs

L’infrastructure réseau de l’entreprise se compose de deux parties principales : le réseau local (LAN) et le réseau hébergé dans le cloud.

Le réseau local est constitué de plusieurs bureaux répartis sur différents sites, non interconnectés entre eux. Chaque bureau dispose de sa propre connexion Internet, fournie soit par une Flybox Orange, soit par une connexion Starlink, selon la couverture réseau disponible. À l’intérieur de chaque site, les ordinateurs et imprimantes sont reliés à un commutateur (*switch*) qui assure l’interconnexion des équipements et leur liaison avec la passerelle Internet. Cette configuration permet de garantir une connectivité stable et fiable pour l’ensemble des utilisateurs, y compris dans les zones à faible couverture réseau.

#### c) Réseau dans le cloud

Les serveurs de l’entreprise sont hébergés chez plusieurs fournisseurs de services situés en France (OVH, SoYouStart, Ikoula, IONOS). Ils sont organisés en six groupes principaux :

- **Serveurs applicatifs :** ils hébergent les applications internes et métiers utilisées par l’entreprise ;
- **Serveurs clients :** ils assurent l’hébergement des sites web et applications destinés aux clients ;
- **Serveurs de sauvegarde :** ils stockent les copies de sauvegarde des données des applications et des clients ;
- **Serveur de fichiers :** il facilite le partage et la synchronisation des fichiers entre les différentes équipes et serveurs ;
- **Serveurs de secours :** ils répliquent les applications critiques et prennent le relais en cas de défaillance des serveurs principaux ;
- **Serveurs de répartition de charge (*load balancing*) :** ils optimisent la distribution du trafic et garantissent la disponibilité continue des services.

Cette architecture garantit une haute disponibilité, une sécurité renforcée, une continuité de service et une gestion centralisée des applications et données critiques.

#### d) Types de réseaux et connexions Internet

L’entreprise utilise deux types de réseaux : le réseau local (LAN) et le réseau étendu (WAN).

Au sein du site principal, les employés utilisent un réseau filaire d’une capacité de 100 Mbit/s. Les connexions sont établies à l’aide de câbles RJ45 de catégorie 5, reliant les ordinateurs, les routeurs et les commutateurs. Le câblage est de type droit pour les connexions entre les postes de travail et le commutateur, et croisé pour les liaisons directes entre deux machines.

Chaque bureau dispose de sa propre passerelle Internet, assurée soit par une Flybox Orange, soit par une connexion Starlink, garantissant une redondance et une stabilité du service même en cas de coupure d’un fournisseur.

Le réseau étendu (WAN) connecte les serveurs hébergés en France aux bureaux locaux via une connexion VPN sécurisée, permettant aux équipes d’accéder en toute sécurité aux environnements de préproduction et de production dans le cloud.

#### e) Serveurs

L’entreprise s’appuie sur une infrastructure de serveurs performante et redondante pour héberger et gérer ses différentes plateformes applicatives. Ces serveurs sont principalement hébergés dans les datacenters de SoYouStart (OVH Cloud), réputés pour leur fiabilité et leurs performances.

À la suite d’un incident majeur survenu dans un datacenter d’OVH en mars 2021, l’entreprise a renforcé sa politique de sauvegarde et de continuité d’activité. Les sauvegardes des données sont désormais répliquées dans les datacenters d’Ikoula, tandis que des serveurs de secours sont hébergés chez IONOS afin d’assurer une reprise rapide des services en cas de panne. L’infrastructure actuelle compte 40 serveurs, répartis selon les rôles présentés dans le tableau 13.

@tabcap Répartition des serveurs selon leur rôle
@colw 3,1
| Rôle du serveur | Nombre |
|---|---|
| Plateforme principale | 16 |
| Plateforme secondaire | 1 |
| Site web institutionnel | 1 |
| Atelier de développement logiciel | 2 |
| GitLab et gestion des sources | 1 |
| Applications clients | 8 |
| Répartition de charge (*load balancer*) | 2 |
| Sauvegardes et réplications | 6 |
| Serveurs de secours | 3 |

La figure 9 donne une vue d’ensemble de cette topologie.

@img fig_etude/p034_n010.png | 0.95 | Topologie globale de l’infrastructure de l’entreprise

## 4.2. Problématique

L’application GESCOM, telle qu’elle existe aujourd’hui, est construite selon une architecture monolithique, avec une base de données fortement couplée et le framework PHP CodeIgniter. Son cycle de développement reste dépendant d’un poste local, les déploiements sont manuels via des *pull* de la branche *master*, et les tests sont majoritairement effectués manuellement sur les nouvelles fonctionnalités, laissant un risque élevé pour les fonctionnalités existantes.

Cette organisation limite la flexibilité, la scalabilité et la rapidité des mises à jour, tout en rendant la maintenance complexe et sensible aux erreurs humaines.

Dans ce contexte, la problématique est la suivante : **comment concevoir et mettre en œuvre une architecture moderne, modulaire et indépendante des contraintes du monolithe, qui permette de fiabiliser le cycle de développement, de déploiement et de test, tout en assurant la continuité et la qualité des mises à jour d’une application de gestion commerciale ?**

## 4.3. Proposition de solution

Pour dépasser les limites du monolithe, il est proposé de migrer vers une architecture modulaire, où chaque fonctionnalité majeure devient un service autonome disposant de sa propre base de données. Cette approche réduit le couplage, facilite la maintenance et limite les risques de régression. L’architecture microservices permet une organisation du développement orientée composants, où chaque équipe est responsable de l’intégralité du cycle de vie de son service et peut choisir le langage de programmation adapté à celui-ci.

Un pipeline CI/CD automatisé assurera la construction, l’exécution des tests et le déploiement de chaque service, garantissant que seules les fonctionnalités validées sont mises en production. Les tests automatisés, notamment fonctionnels et de bout en bout avec Cypress, permettront de couvrir à la fois les nouvelles fonctionnalités et les fonctions critiques existantes, améliorant ainsi la qualité globale.

L’infrastructure sera conteneurisée avec Docker et orchestrée via Kubernetes, garantissant la portabilité, la scalabilité et la tolérance aux pannes. L’objectif est de rendre le cycle de vie de l’application plus modulaire, fiable et automatisé, et d’assurer la continuité des services ainsi que la qualité des mises à jour.

@chapter Chapitre 5. Études théoriques et choix des outils

Afin de mettre en œuvre une architecture modulaire et automatisée, il est nécessaire de choisir des outils adaptés à chaque étape du cycle de développement, de déploiement et de test. Ce chapitre présente les notions fondamentales du projet, les outils envisagés, leur comparaison et les choix retenus.

## 5.1. Notions de microservices

L’architecture microservices constitue aujourd’hui l’un des paradigmes les plus utilisés pour la conception d’applications modernes, flexibles et évolutives [1][6]. Contrairement à l’architecture monolithique, où toutes les fonctionnalités d’une application sont regroupées au sein d’un seul bloc, le modèle microservices repose sur la décomposition du système en plusieurs services indépendants, chacun ayant une responsabilité spécifique et communiquant généralement via des API légères, souvent en REST ou en GraphQL.

Chaque microservice peut être développé, testé, déployé et mis à jour de manière autonome, ce qui favorise l’agilité et la rapidité des cycles de développement. De plus, les équipes peuvent choisir des langages, frameworks ou bases de données adaptés aux besoins spécifiques de chaque service, sans dépendre d’une technologie unique. Cette indépendance technologique améliore la maintenabilité et permet une meilleure répartition des charges de travail entre les équipes.

Les microservices offrent également une grande résilience : en cas de défaillance d’un service, le reste de l’application continue de fonctionner, ce qui renforce la fiabilité globale du système. Ils facilitent aussi la scalabilité horizontale : il est possible d’augmenter les ressources uniquement pour les services les plus sollicités, sans impacter l’ensemble de l’application.

Cependant, cette approche introduit une certaine complexité, notamment dans la gestion de la communication entre services, la supervision, la sécurité et le déploiement. C’est pourquoi elle est souvent associée à des outils d’orchestration comme Kubernetes, à des systèmes de CI/CD pour automatiser les mises à jour, et à des outils de supervision pour assurer une visibilité complète sur le comportement des services.

En somme, les microservices favorisent la modularité, la flexibilité et la résilience des applications, tout en exigeant une infrastructure bien pensée et automatisée pour en exploiter pleinement le potentiel.

## 5.2. Gestionnaire de versions

Un gestionnaire de versions est un outil qui permet de suivre et de gérer les modifications apportées aux fichiers d’un projet, généralement du code source. Le tableau 14 compare les principaux outils existants.

@tabcap Comparaison des gestionnaires de versions
@colw 1,0.9,1.5,1.5,1.4
| Outil | Type | Avantages | Limites | Cas d’utilisation typique |
|---|---|---|---|---|
| **Git** [7] | Distribué | Branches flexibles, travail hors ligne, intégration CI/CD, adoption massive | Courbe d’apprentissage initiale, complexité des commandes avancées | Projets collaboratifs, DevOps, microservices |
| **Mercurial** | Distribué | Interface simple, travail hors ligne, versionnage fiable | Moins répandu, communauté plus réduite | Projets moyens ou équipes recherchant la simplicité |
| **Subversion (SVN)** | Centralisé | Simple à utiliser, historique et permissions centralisés | Pas de travail hors ligne complet, création de branches et fusion plus difficiles | Projets mono-équipe, environnements d’entreprise traditionnels |
| **CVS** | Centralisé | Historique centralisé, simple à configurer | Très ancien, peu flexible, faible support | Projets historiques ou maintenance d’anciens logiciels |

Pour ce projet, **Git** est retenu pour sa flexibilité, son intégration naturelle avec les pipelines CI/CD, sa large communauté et sa capacité à gérer efficacement le développement distribué et les microservices [5].

Git est l’un des systèmes de gestion de versions les plus utilisés dans le développement logiciel. Il conserve l’historique complet des modifications, permet de comparer différentes versions et de revenir à un état antérieur si nécessaire. Dans le cadre de ce projet, Git permettra de :

- suivre toutes les modifications du code et des configurations ;
- restaurer une version précédente en cas d’erreur ou de bug critique ;
- faciliter la collaboration entre plusieurs développeurs travaillant sur différents services ;
- intégrer le code avec les outils de CI/CD pour automatiser les tests et le déploiement.

L’utilisation de Git est essentielle pour assurer la traçabilité, la sécurité et la fiabilité du code. Elle permet de réduire les risques de conflits, de gérer efficacement les corrections et les améliorations, et de conserver un historique complet, indispensable à la maintenance et à l’évolution d’une application modulaire. Par exemple :

- un développeur peut corriger un bug dans un service et valider (*commit*) les changements avec un message décrivant la modification ;
- l’équipe peut cloner le dépôt pour travailler localement, puis pousser (*push*) les modifications sur le serveur central pour intégration ;
- Git permet également d’étiqueter (*tag*) des versions stables avant chaque mise en production afin de pouvoir revenir facilement à une version précédente si nécessaire.

## 5.3. Conteneurisation

La conteneurisation est une technique permettant d’isoler une application et toutes ses dépendances dans un conteneur léger et portable, garantissant qu’elle fonctionne de manière identique quel que soit l’environnement. Docker est la plateforme de conteneurisation la plus utilisée ; elle facilite la création, le déploiement et l’exécution d’applications dans des environnements isolés [8]. Le tableau 15 compare les principales solutions.

@tabcap Comparaison des solutions de conteneurisation
@colw 1,1.1,1.6,1.5,1.4
| Outil | Type | Avantages | Limites | Cas d’utilisation typique |
|---|---|---|---|---|
| **Docker** [8] | Conteneurisation légère | Isolation des applications, portabilité, images reproductibles, large écosystème, intégration CI/CD | Consommation mémoire si trop de conteneurs, sécurité dépendante du noyau hôte | Microservices, CI/CD, tests automatisés, déploiement en cloud ou en local |
| **Podman** | Conteneurisation légère sans démon | Pas de démon root, compatible avec la CLI Docker, sécurisé | Communauté moins large, outils d’orchestration moins matures | Environnements sensibles à la sécurité, microservices isolés |
| **LXC/LXD** | Conteneurs système | Isolation complète, virtualisation légère, simule un OS entier | Complexité de configuration, moins adapté aux microservices | Virtualisation de serveurs, tests de systèmes complets |
| **rkt (Rocket)** | Conteneurisation orientée sécurité | Sécurisé, intégration avec Kubernetes | Moins populaire, fin du support officiel | Déploiements sécurisés, expérimentations avec Kubernetes |

**Docker** est retenu pour ce projet grâce à sa simplicité, sa compatibilité avec Kubernetes, son écosystème riche et sa facilité d’intégration dans les pipelines CI/CD. Il permettra de construire, tester et déployer rapidement les microservices dans un environnement cohérent et portable. Docker est utilisé pour :

- isoler chaque service de l’application (clients, articles, facturations) afin qu’ils puissent fonctionner indépendamment ;
- assurer la cohérence entre les environnements de développement, de test et de production ;
- simplifier le déploiement et la mise à jour des services sans affecter les autres parties de l’application ;
- faciliter la création d’environnements de test pour valider les correctifs avant la mise en production.

La conteneurisation permet d’améliorer la portabilité, la scalabilité et la résilience des applications. Chaque service peut être démarré, arrêté ou mis à jour indépendamment, ce qui réduit les risques de régression. Docker est également un élément clé de toute infrastructure DevOps, car il s’intègre facilement dans les pipelines CI/CD et dans des systèmes d’orchestration comme Kubernetes. Par exemple :

- un développeur peut créer un conteneur Docker contenant un service de gestion des articles avec toutes ses dépendances et le tester localement sans modifier son environnement principal ;
- lors de la mise en production, ce même conteneur peut être déployé sur le serveur de manière identique, garantissant un comportement prévisible ;
- Docker permet également de lancer simultanément plusieurs conteneurs pour simuler l’intégration de différents services de l’application dans un environnement de test complet.

## 5.4. Notions d’intégration continue et de déploiement continu

L’intégration continue (CI) et le déploiement continu (CD) sont deux pratiques fondamentales du DevOps, visant à automatiser le cycle de vie des applications pour le rendre plus fiable, rapide et reproductible [2][3].

L’intégration continue consiste à fusionner régulièrement les modifications de code provenant de différents développeurs dans un dépôt centralisé. Chaque modification déclenche automatiquement des tests unitaires, fonctionnels et de conformité, ce qui permet de détecter rapidement les erreurs ou les conflits avant qu’ils n’affectent l’ensemble du système.

Le déploiement continu, quant à lui, permet de mettre automatiquement à disposition les modifications validées dans des environnements de test, de préproduction ou directement de production. Cette pratique garantit que chaque nouvelle fonctionnalité ou correction de bug est rapidement et sûrement disponible pour les utilisateurs finaux, tout en maintenant la stabilité de l’application.

La CI et le CD sont donc complémentaires : la CI se concentre sur la qualité et la validation du code, tandis que le CD s’assure de sa livraison fiable et rapide. Dans le cadre d’une application modulaire, l’intégration et le déploiement continus permettent de :

- vérifier automatiquement la compatibilité et la stabilité de chaque service indépendamment ;
- détecter immédiatement les régressions et les erreurs après chaque modification, réduisant ainsi les risques pour la production ;
- déployer rapidement de nouvelles fonctionnalités ou des correctifs sur les environnements de test et de préproduction avant leur mise en production ;
- maintenir la cohérence entre les différents environnements et faciliter la collaboration entre plusieurs développeurs travaillant sur des services distincts.

La CI/CD est essentielle pour améliorer la qualité globale du logiciel, réduire les risques liés aux erreurs humaines et accélérer le cycle de développement et de mise en production. Elle favorise également la traçabilité complète des changements, permet de générer des *builds* reproductibles et d’assurer la cohérence entre les environnements locaux, de test et de production. Dans un projet basé sur une architecture modulaire et conteneurisée, ces pratiques sont indispensables pour gérer efficacement les services indépendants, automatiser les tests et orchestrer les déploiements. Par exemple :

- lorsqu’un développeur pousse une modification sur le dépôt Git, un serveur CI/CD déclenche automatiquement la construction et l’exécution des tests du service concerné, garantissant que tout fonctionne avant la fusion ;
- si les tests sont validés, le pipeline déploie automatiquement le service dans un environnement de préproduction ou de production, sans intervention manuelle ;
- en cas d’échec d’un test, le pipeline bloque le déploiement et alerte l’équipe, permettant une correction rapide et évitant que le bug n’atteigne les utilisateurs ;
- les pipelines CI/CD peuvent également générer automatiquement des rapports de test et des artefacts (images Docker, fichiers de configuration) pour assurer la traçabilité et faciliter la maintenance.

Grâce à l’intégration et au déploiement continus, le projet bénéficie d’une agilité accrue, d’une réduction du délai entre le développement et la production, et d’une qualité logicielle améliorée. Le tableau 16 compare les principales plateformes de CI/CD.

@tabcap Comparaison des plateformes de CI/CD
@colw 1,1,1.6,1.4,1.4
| Outil / Plateforme | Type | Avantages | Limites | Cas d’utilisation typique |
|---|---|---|---|---|
| **GitHub Actions** [9] | CI/CD intégré à GitHub | Intégré au dépôt, facile à configurer, YAML déclaratif, exécutions automatisées sur *push* et *pull request* | Limité aux dépôts GitHub, ressources gratuites limitées | Microservices, pipelines CI/CD rapides, tests et déploiements automatisés |
| **GitLab CI/CD** | CI/CD intégré à GitLab | Intégré au dépôt, *runners* personnalisables, YAML déclaratif | Complexité pour les déploiements externes, courbe d’apprentissage | Projets internes, pipelines complexes, multi-langages |
| **Jenkins** | Serveur CI/CD autonome | Très flexible, nombreux plugins, large adoption | Installation et maintenance complexes, nécessite un serveur dédié | Projets de grande envergure, environnements hétérogènes |
| **CircleCI** | CI/CD en SaaS | Cloud ou sur site, pipelines rapides, intégration Docker | Limité hors cloud, coût pour un usage intensif | Déploiements cloud, pipelines automatisés pour microservices |

Pour ce projet, **GitHub Actions** est retenu grâce à sa facilité d’intégration avec les dépôts GitHub, sa configuration déclarative via YAML et sa capacité à automatiser les tests et les déploiements des microservices. Cette solution permet de construire un pipeline CI/CD complet, garantissant la cohérence et la fiabilité des versions déployées.

## 5.5. Notions d’orchestration

L’orchestration désigne l’ensemble des mécanismes et outils permettant d’automatiser la gestion, la coordination et la supervision des conteneurs au sein d’une infrastructure distribuée. Elle consiste à planifier le déploiement, la montée en charge, la mise à jour et la tolérance aux pannes des services, tout en garantissant la stabilité et la continuité du système.

Dans une architecture basée sur des microservices, où chaque composant fonctionne dans son propre conteneur, l’orchestration est indispensable pour gérer efficacement les ressources et les communications entre services. Elle intervient à plusieurs niveaux du cycle de vie des applications :

- automatisation du déploiement de conteneurs sur différents environnements (développement, test, production) ;
- gestion de la scalabilité, en ajustant dynamiquement le nombre d’instances en fonction de la charge ;
- supervision de l’état des conteneurs et redémarrage automatique en cas de défaillance pour assurer la haute disponibilité ;
- administration du réseau interne entre les services conteneurisés (attribution d’adresses IP, ouverture de ports, politiques de sécurité) ;
- mise à jour continue des services via des stratégies de déploiement sans interruption (*rolling updates*).

L’orchestration constitue un pilier central d’une infrastructure DevOps moderne. Elle permet d’obtenir un système automatisé, hautement disponible et résilient, en réduisant les interventions manuelles et les erreurs humaines. Grâce à elle, les applications deviennent plus faciles à maintenir, à faire évoluer et à adapter aux besoins en ressources. Elle assure également une gestion centralisée des configurations et des ressources, tout en améliorant la scalabilité horizontale des applications conteneurisées. Par exemple :

- un orchestrateur peut déployer automatiquement plusieurs conteneurs d’une même application sur différents serveurs physiques ou virtuels ;
- en cas d’échec d’un conteneur, celui-ci est redémarré automatiquement sans affecter les autres services ;
- lors du déploiement d’une nouvelle version, l’orchestrateur effectue une mise à jour progressive pour éviter toute interruption ;
- des fichiers de configuration (souvent en YAML) décrivent le comportement de chaque service, rendant les déploiements reproductibles et standardisés.

Ainsi, l’orchestration représente une composante essentielle de la gestion d’applications conteneurisées à grande échelle. Elle garantit non seulement la continuité de service, mais aussi la flexibilité et l’efficacité opérationnelle nécessaires à la mise en œuvre des pratiques DevOps.

## 5.6. Choix de la solution de virtualisation

La virtualisation est une technologie fondamentale qui consiste à créer une version virtuelle d’une ressource physique telle qu’un serveur, un système d’exploitation, un espace de stockage ou un réseau. Elle permet de faire fonctionner plusieurs environnements isolés sur une même machine physique, favorisant ainsi une utilisation optimale des ressources matérielles.

Son principe repose sur la séparation entre le matériel et les environnements logiciels, rendant possible la création de plusieurs machines virtuelles indépendantes, chacune disposant de son propre système d’exploitation et de ses applications. Cette abstraction simplifie considérablement la gestion, la maintenance et le déploiement des environnements informatiques.

Dans le contexte du DevOps et du développement applicatif moderne, la virtualisation offre de nombreux avantages. Elle permet notamment de reproduire fidèlement les environnements de production, de tester différentes configurations sans perturber l’infrastructure principale et d’assurer une meilleure isolation entre les services. Grâce à cette approche, les équipes de développement et d’exploitation gagnent en flexibilité et en rapidité, tout en réduisant les risques liés aux incompatibilités d’environnement. Le tableau 17 compare les principales solutions.

@tabcap Comparaison des solutions de virtualisation
@colw 1.1,1,1.5,1.4,1.4
| Outil | Type | Avantages | Limites | Cas d’utilisation typique |
|---|---|---|---|---|
| **VirtualBox** [12] | Virtualisation complète | Open source, multiplateforme, simple à configurer, bonne intégration avec Vagrant | Moins performant pour de très gros clusters, consommation mémoire importante | Machines de test, environnements locaux de développement, clusters Kubernetes légers |
| **VMware Workstation / Player** | Virtualisation complète | Performances élevées, fonctionnalités avancées, instantanés (*snapshots*) | Payant pour la version complète, moins simple à automatiser | Environnements de test et de production nécessitant robustesse et support |
| **Hyper-V** | Virtualisation intégrée à Windows | Intégré à Windows, bonnes performances, instantanés | Limité aux hôtes Windows, moins flexible pour Linux | Tests et développement sur machines Windows |
| **KVM / QEMU** | Virtualisation Linux | Très performant, open source, flexible | Complexité de configuration, interface moins conviviale | Déploiement de serveurs Linux, virtualisation à grande échelle |

**VirtualBox** est retenu pour sa simplicité d’utilisation, sa compatibilité multiplateforme et son intégration avec Vagrant [11]. Cette combinaison permet de provisionner rapidement des machines virtuelles identiques et de reproduire un cluster Kubernetes complet.

## 5.7. Scripts YAML

Les scripts YAML (*YAML Ain’t Markup Language*) sont largement utilisés pour décrire des configurations de manière lisible et structurée [18]. Dans le contexte du DevOps, ils jouent un rôle essentiel dans l’automatisation des processus d’intégration et de déploiement continus. Ces fichiers permettent de définir, étape par étape, le comportement d’un pipeline : compilation, tests, génération d’images, déploiement ou encore notifications.

Un exemple concret d’utilisation de YAML se retrouve dans les *workflows* GitHub, au cœur de GitHub Actions. Ce système permet d’automatiser des tâches à chaque événement du cycle de développement, comme un *push*, une *pull request* ou une *release*. Le fichier YAML, placé dans le répertoire `.github/workflows/`, décrit la suite des actions à exécuter dans un ordre précis, les environnements utilisés (Node.js, Python, Docker…) ainsi que les conditions de déclenchement.

Grâce à cette approche déclarative, les équipes peuvent mettre en place des pipelines reproductibles et faciles à maintenir, sans nécessiter de serveur d’intégration dédié. Les *workflows* GitHub s’intègrent naturellement aux dépôts de code, favorisant la transparence, la collaboration et la traçabilité des déploiements. Ainsi, l’usage des scripts YAML constitue un élément clé de l’automatisation DevOps moderne, garantissant la cohérence et la fiabilité des processus de CI/CD.

## 5.8. Plateformes d’orchestration de conteneurs Docker

L’orchestration de conteneurs est une composante essentielle de la gestion d’applications modernes déployées sous forme de microservices. Elle vise à automatiser la mise en œuvre, la gestion, la mise à l’échelle et la supervision des conteneurs, afin d’assurer une disponibilité continue et une répartition optimale des ressources.

Lorsqu’un projet comporte plusieurs conteneurs interdépendants, la gestion manuelle devient rapidement complexe. Les plateformes d’orchestration permettent alors de définir des stratégies de déploiement, de gérer les dépendances entre services, de surveiller leur état et d’assurer une tolérance aux pannes. Elles prennent également en charge la mise à jour continue (*rolling updates*), la reprise automatique après incident (*self-healing*) et le dimensionnement dynamique selon la charge du système. Le tableau 18 compare les principales plateformes.

@tabcap Comparaison des plateformes d’orchestration de conteneurs
@colw 1.1,1,1.5,1.4,1.4
| Outil / Plateforme | Type | Avantages | Limites | Cas d’utilisation typique |
|---|---|---|---|---|
| **Kubernetes** [10] | Orchestration complète | Scalabilité, tolérance aux pannes, gestion déclarative des ressources, large communauté et écosystème riche | Courbe d’apprentissage élevée, configuration complexe pour les débutants | Microservices, clusters distribués, déploiements en production et en test |
| **Docker Swarm** | Orchestration intégrée à Docker | Facile à configurer, intégré à la CLI Docker, adapté aux petites architectures | Fonctionnalités avancées limitées, moins adapté aux grands clusters | Projets de petite à moyenne taille, prototypes ou POC |
| **Apache Mesos / Marathon** | Orchestration distribuée | Très scalable, gestion de ressources multi-applications | Complexité de configuration, communauté moins active | Grands environnements multi-services, applications distribuées complexes |
| **Nomad (HashiCorp)** | Orchestration légère | Simplicité, multi-cloud, intégration facile avec Consul | Fonctionnalités avancées limitées par rapport à Kubernetes | Petits clusters, charges de travail hétérogènes |

Parmi ces solutions, Kubernetes s’impose comme la référence du domaine [4]. Développé initialement par Google, il offre une approche déclarative de la gestion d’infrastructure et prend en charge l’automatisation complète du cycle de vie des conteneurs Docker. Il permet notamment la gestion de clusters distribués, le déploiement évolutif et la surveillance centralisée des services. D’autres outils comme Docker Swarm ou Apache Mesos proposent des fonctionnalités similaires, mais Kubernetes se distingue par sa robustesse, sa communauté active et son écosystème étendu.

**Kubernetes** est donc retenu pour sa robustesse, sa capacité à gérer un cluster complet de microservices et sa compatibilité avec Docker. Il permet de déployer les services de manière scalable, résiliente et automatisée, tout en offrant un environnement proche de la production pour tester et orchestrer les microservices.
