@front INTRODUCTION GÉNÉRALE
@mode arabic reset

L’évolution rapide des technologies de l’information a profondément modifié la manière de concevoir, développer et déployer les applications. Face à la complexité croissante des systèmes monolithiques, les entreprises recherchent aujourd’hui des solutions leur permettant d’assurer rapidité, fiabilité et continuité dans le cycle de vie logiciel. L’architecture microservices, associée aux pratiques DevOps, répond à ces besoins en favorisant la modularité, l’automatisation et la flexibilité du développement. Cependant, la gestion de plusieurs services indépendants peut s’avérer complexe.

Ce projet a pour but de concevoir et de mettre en œuvre une infrastructure d’intégration et de déploiement continus (CI/CD) spécifiquement adaptée à une application reposant sur une architecture microservices. Il vise à automatiser et à optimiser le processus de livraison logicielle tout en garantissant la fiabilité et la cohérence des déploiements. En intégrant un mécanisme d’orchestration des services, cette infrastructure permettra également d’assurer une meilleure gestion des ressources, une scalabilité accrue et une haute disponibilité de l’application dans son ensemble.

Dès lors, comment automatiser de manière fiable l’intégration, le test et le déploiement d’une application composée de plusieurs services indépendants, tout en garantissant sa disponibilité et sa capacité à s’adapter à la charge ?

Le présent mémoire est structuré en trois grandes parties. La première partie introduit le cadre général du travail en présentant l’École Nationale d’Informatique, l’entreprise d’accueil et la description du projet. La deuxième partie traite de l’analyse de l’existant, de la problématique identifiée et du choix des technologies et outils retenus pour la mise en œuvre du pipeline CI/CD et de l’orchestration. Enfin, la troisième partie expose les différentes étapes de réalisation du projet, de l’installation et de la configuration des outils jusqu’à la vérification des déploiements et des résultats obtenus. Une conclusion générale récapitule les principaux acquis de ce travail et ouvre des perspectives d’amélioration.

@part PARTIE I. PRÉSENTATIONS

@chapter Chapitre 1. Présentation de l’ENI

L’École Nationale d’Informatique (ENI) est reconnue comme un établissement de référence à Madagascar dans le domaine de la formation en informatique.

## 1.1. Information d’ordre général

L’École Nationale d’Informatique, en abrégé ENI, est un établissement d’enseignement supérieur rattaché académiquement et administrativement à l’Université de Fianarantsoa. Le siège de l’École se trouve à Tanambao-Antaninarenina à Fianarantsoa. L’adresse pour la prise de contact avec l’École est la suivante : École Nationale d’Informatique (ENI) Tanambao, Fianarantsoa. Le numéro de sa boîte postale est 1487 avec le code postal 301. Téléphone : 038 96 566 96 ou 034 76 591 95. Son adresse électronique est la suivante : **eni@eni.mg**. Elle dispose également d’un site web : **www.eni.mg**.

## 1.2. Missions et historique

L’ENI se positionne sur l’échiquier socio-éducatif malgache comme étant le plus puissant secteur de diffusion et de vulgarisation des connaissances et des technologies informatiques. Cette École Supérieure peut être considérée aujourd’hui comme la vitrine et la pépinière des élites informaticiennes du pays.

De façon formelle, l’ENI a été créée par le décret N° 83-185 du 24 mai 1983, comme étant le seul établissement universitaire professionnalisé au niveau national, destiné à former des techniciens et des ingénieurs de haut niveau, aptes à répondre aux besoins et exigences d’informatisation des entreprises, des sociétés et des organes implantés à Madagascar.

L’ENI a par conséquent pour mission de former des spécialistes informaticiens compétents et opérationnels de différents niveaux, notamment :

- en fournissant à des étudiants des connaissances de base en informatique ;
- en leur transmettant le savoir-faire requis, à travers la professionnalisation des formations dispensées et en essayant d’assurer une meilleure adéquation des formations par rapport aux besoins évolutifs des sociétés et des entreprises ;
- en initiant les étudiants aux activités de recherche dans les différents domaines des Technologies de l’Information et de la Communication (TIC).

La filière de formation d’Analystes Programmeurs a été mise en place à l’École en 1983, et a été gelée par la suite en 1996, tandis que la filière de formation d’ingénieurs a été ouverte à l’École en 1986.

Une formation de troisième cycle a été ouverte à l’École depuis l’année 2003-2004 grâce à la coopération académique et scientifique entre l’Université de Fianarantsoa, pour le compte de l’ENI, et l’Université Paul Sabatier de Toulouse (UPST). Cette filière avait pour objectif de former certains étudiants à la recherche dans les différents domaines de l’informatique, et notamment de préparer la relève des enseignants-chercheurs qui étaient en poste.

Pendant l’année 2007-2008, la formation en vue de l’obtention du diplôme de Licence Professionnelle en Informatique a été mise en place à l’ENI avec les deux parcours de formation :

- Génie Logiciel et Base de Données ;
- Administration des Systèmes et Réseaux.

La mise en place à l’École de ces deux options de formation devait répondre au besoin de basculement vers le système Licence – Master – Doctorat (LMD).

En vue de surmonter les difficultés de limitation de l’effectif des étudiants accueillis à l’École, notamment à cause du manque d’infrastructures, un système de « Formation Hybride » a été mis en place à partir de l’année 2010. Il s’agit en effet d’un système de formation semi-présentielle et à distance avec l’utilisation de la visioconférence pour la formation à distance. Le système de formation hybride a ainsi été créé à Fianarantsoa ainsi qu’à l’Université de Toliara. Cette formation est à l’origine du parcours Informatique Générale.

En 2023, la mention Intelligence Artificielle (IA) a été ouverte au sein de l’École pour répondre aux besoins des entreprises. La formation est destinée aux étudiants titulaires du diplôme de licence (Bac +3) en mathématiques, en statistiques ou en informatique. La mention IA comporte deux parcours :

- Gouvernance et Ingénierie de Données (GID) ;
- Objets Connectés et Cybersécurité (OCC).

Le parcours GID offre aux étudiants des compétences scientifiques et techniques spécialisées en science des données. Le parcours OCC confère aux étudiants une double spécialité, d’abord en internet des objets, ensuite en cybersécurité. La formation de master est axée sur l’ensemble des applications de l’intelligence artificielle.

Depuis l’année universitaire 2024-2025, la mention Expertise Digitale est officiellement ouverte au grand public. Cette mention propose deux (2) parcours distincts :

- **Métiers du Digital (MDi)** – disponible aux niveaux Licence et Master. Ce parcours est destiné aux étudiants titulaires du diplôme de Baccalauréat, toutes séries confondues. Il est élaboré pour équiper les étudiants des compétences essentielles dans les domaines du marketing digital, de la communication digitale et de la gestion de projets digitaux.
- **Audit des Systèmes d’Information (ASI)** – proposé au niveau Master uniquement. Ce parcours s’adresse aux étudiants titulaires d’une licence (Bac +3) en mathématiques, en statistiques ou en informatique. Il est structuré pour approfondir les connaissances théoriques et pratiques nécessaires à l’audit efficace des systèmes d’information.

Le système d’enseignement adopté pour cette mention est un système en ligne. Ainsi, les cours et ressources pédagogiques sont accessibles en permanence via la plateforme numérique Moodle. Par ailleurs, des regroupements en présentiel ou en ligne sont organisés périodiquement, conformément au planning défini par les responsables pédagogiques.

## 1.3. Organigramme institutionnel

L’organigramme de l’École est inspiré des dispositions du décret N° 83-185 du 24 mai 1983. L’ENI est administrée par un Conseil d’École, et dirigée par un directeur nommé par un décret adopté en Conseil des Ministres. Le Collège des enseignants, regroupant tous les enseignants-chercheurs permanents de l’École, est chargé de résoudre les problèmes liés à l’organisation pédagogique des enseignements. Le Conseil Scientifique propose les orientations pédagogiques et scientifiques de l’établissement, en tenant compte notamment de l’évolution du marché du travail et de l’adéquation des formations dispensées par rapport aux besoins des entreprises.

La figure 1 représente l’organigramme actuel de l’École Nationale d’Informatique.

@img fig_etude/p013_n000.png | 0.85 | Organigramme de l’École Nationale d’Informatique

## 1.4. Domaines de spécialisation

Les activités de formation et de recherche organisées à l’ENI portent sur les domaines suivants :

- Génie Logiciel et Base de Données ;
- Administration des Systèmes et Réseaux ;
- Informatique Générale ;
- Modélisation informatique et mathématique des systèmes complexes ;
- Intelligence artificielle.

Le tableau 1 décrit l’organisation du système de formation pédagogique de l’École.

@tabcap Organisation du système de formation pédagogique de l’École
@colw 1,1
| Formation théorique | Formation pratique |
|---|---|
| • Enseignement théorique<br>• Travaux dirigés<br>• Travaux pratiques<br>• Conférences | • Études de cas<br>• Travaux de réalisation<br>• Projets / Projets tutorés<br>• Voyages d’études<br>• Stages en entreprise |

## 1.5. Architecture des formations pédagogiques

Le recrutement des étudiants à l’ENI se fait uniquement par voie de concours d’envergure nationale en première année. Les offres de formation organisées à l’École ont été validées par la Commission Nationale d’Habilitation (CNH). Au sein de l’ENI, il existe trois mentions et sept parcours. Le tableau 2 récapitule les mentions et les parcours au sein de l’École.

@tabcap Mentions et parcours au sein de l’ENI
@colw 1,1.6
| Mention | Parcours |
|---|---|
| **Informatique** | Génie Logiciel et Base de Données (GB)<br>Administration des Systèmes et Réseaux (ASR)<br>Informatique Générale (IG) |
| **Intelligence Artificielle** | Gouvernance et Ingénierie de Données (GID)<br>Objets Connectés et Cybersécurité (OCC) |
| **Expertise Digitale** | Métiers du Digital (MDi)<br>Audit des Systèmes d’Information (ASI) |

La figure 2 représente l’architecture des études correspondant au système LMD.

@img fig_bokyy/p008_n004.png | 0.65 | Architecture des études correspondant au système LMD

La licence peut avoir une vocation générale ou professionnelle. Le master peut avoir une vocation professionnelle ou de recherche. L’accès en première année de master se fait automatiquement pour les étudiants de l’École qui ont obtenu le diplôme de Licence Professionnelle.

Le tableau 3 illustre la liste des formations existantes à l’ENI.

@tabcap Liste des formations existantes à l’ENI
@colw 1,1.3,1.5
| Formation | Licence professionnelle | Master |
|---|---|---|
| **Condition d’admission** | Par voie de concours | Par voie de concours pour la mention IA |
| **Condition d’accès** | Bac de série C, D ou Technique | Être titulaire d’une licence professionnelle |
| **Durée de formation** | 3 ans | 2 ans |
| **Diplôme délivré** | Diplôme de Licence Professionnelle | Diplôme de Master Professionnel<br>Diplôme de Master Recherche |

Le Master Recherche permet à son titulaire de poursuivre directement des études en doctorat et de s’inscrire directement dans une École Doctorale. Les étudiants diplômés de l’École sont plutôt bien accueillis dans les instituts universitaires étrangers (Canada, Suisse, France…).

## 1.6. Relation de l’ENI avec les organismes externes

Les stages effectués chaque année par les étudiants mettent l’École en rapport permanent avec plus de 400 entreprises et organismes publics, semi-publics et privés, nationaux et internationaux. L’École dispose ainsi d’un réseau d’entreprises, de sociétés et d’organismes publics et privés qui sont des partenaires par l’accueil en stage de ses étudiants, et éventuellement pour le recrutement après l’obtention des diplômes. Les compétences que l’École cherche à développer chez ses étudiants sont l’adaptabilité, le sens de la responsabilité, le travail en équipe, le goût de l’expérimentation et l’innovation.

En effet, la vocation de l’ENI est de former des licenciés et des ingénieurs de niveau master avec des qualités scientifiques, techniques et humaines reconnues, capables d’évoluer professionnellement dans des secteurs d’activité variés intégrant l’informatique. Les stages en milieu professionnel permettent de favoriser une meilleure adéquation entre les formations à l’École et les besoins évolutifs du marché de l’emploi.

Parmi les sociétés, les entreprises et les organismes partenaires de l’École, on peut citer : ACCENTURE Mauritius, AKATA Goavana, Air Madagascar, Ambre Associates, Airtel, Agence Universitaire de la Francophonie (AUF), AXIAN, B2B, Banque Centrale, BIANCO, BlueLine, CNaPS, Bureau National de Gestion des Risques et des Catastrophes (BNGRC), CEDII-Fianarantsoa, Data Consulting, Central Test, Centre National Antiacridien, CNRE, COLAS, Direction Générale des Douanes, DLC, E-Tech Consulting, FID, FIHARY Soft, FTM, GNOSYS, GENIUS AT WORK, Hello Tana, IBONIA, INGENOSIA, INSTAT, IOGA, JIRAMA, JOUVE, MADADEV, MAEP, MANAO, MEF, MEN, MESupRES, MFB, MININTER, Ministère des Postes, des Télécommunications et du Développement Numérique, NEOV MAD, Ny Havana, Madagascar National Parks, OMNITEC, ORANGE, OTME, PRACCESS, QMM Fort-Dauphin, SG Madagasikara, SMMC, SMMEC, SNEDADRS Antsirabe, Sénat, Société d’Exploitation du Port de Toamasina (SEPT), SOFTWELL, Strategy Consulting, TELMA, VIVETEC, Société LAZAN’I BETSILEO, WWF, UGD, ARATO, MNDPT, NG ACADEMY, Relia, Spoon Consulting…

## 1.7. Débouchés professionnels des diplômés

Les formations proposées par l’École permettent aux diplômés d’être immédiatement opérationnels sur le marché du travail avec la connaissance d’un métier complet lié à l’informatique et aux TIC. L’École apporte à ses étudiants un savoir-faire et un savoir-être qui les accompagnent tout au long de leur vie professionnelle. Elle a une vocation professionnalisante. Les diplômés en licence et en master issus de l’ENI peuvent faire carrière dans différents secteurs.

L’École bénéficie aujourd’hui de plus de 40 années d’expérience pédagogique et de reconnaissance auprès des sociétés, des entreprises et des organismes. C’est une École Supérieure de référence en matière informatique.

D’une manière générale, les diplômés de l’ENI n’éprouvent pas de difficultés particulières à être recrutés au terme de leurs études. Cependant, l’ENI recommande à ses diplômés de promouvoir l’entrepreneuriat en TIC et de créer des cybercafés, des SSII ou des bureaux d’études. Le tableau 4 représente les débouchés éventuels selon la mention.

@tabcap Débouchés éventuels des jeunes diplômés
@colw 1.45,4
| Mention | Débouchés professionnels |
|---|---|
| **INFORMATIQUE** | **GB :** Développeur logiciel / développeur full-stack, Ingénieur en développement d’applications (desktop, web, mobile), Architecte logiciel, Intégrateur d’applications, Développeur d’API, Administrateur de bases de données (DBA), Ingénieur en conception de bases de données, Développeur SQL / PL-SQL, Spécialiste en migration et optimisation de bases de données, Data engineer, Analyste programmeur, Analyste fonctionnel, Chef de projet informatique, Scrum master / Product owner, Ingénieur QA (Quality Assurance), Testeur logiciel / testeur automatisé, Spécialiste maintenance applicative, Expert en refactoring et optimisation de code, Analyste de données, Concepteur d’outils décisionnels (BI), Ingénieur Big Data, Machine Learning Engineer, Consultant fonctionnel ou freelance.<br>**ASR :** Administrateur systèmes et réseaux, Ingénieur systèmes et réseaux, Administrateur systèmes Linux / Windows, Administrateur cloud (AWS, Azure, Google Cloud), Ingénieur virtualisation (VMware, Hyper-V, Proxmox), Administrateur sécurité, Ingénieur cybersécurité, Analyste SOC, Spécialiste firewall / VPN, RSSI (avec expérience), Technicien support informatique (N2/N3), Technicien réseaux et télécoms, Ingénieur exploitation, Administrateur messagerie, Technicien datacenter, Architecte réseaux, Architecte systèmes, Consultant infrastructure, Chef de projet systèmes et réseaux, Ingénieur DevOps, Administrateur Kubernetes / Docker, Cloud engineer, Spécialiste automatisation (Ansible, Terraform).<br>**IG :** débouchés des parcours GB et ASR à la fois. |
| **INTELLIGENCE<br>ARTIFICIELLE** | **GID :** Développeur IA, Data Scientist, Entrepreneur IA, Consultant IA, Responsable marketing IA, Business Developer IA, Product Owner, Consultant en cybersécurité, Directeur de l’innovation.<br>**OCC :** Analyste en cybersécurité, Ingénieur en cybersécurité, Spécialiste en réponse aux incidents, Architecte de sécurité, Consultant et auditeur en cybersécurité, Expert en sécurité des données, Responsable de la sécurité des informations, Chercheur et formateur en cybersécurité, Ingénieur, développeur et architecte IoT, Spécialiste en sécurité IoT, Analyste de données. |
| **EXPERTISE<br>DIGITALE** | **MDi :** Spécialiste en marketing digital, Gestionnaire de contenu web, Analyste UX/UI, Product Owner, Chef de projet digital, Stratège en médias sociaux, Concepteur-rédacteur web, Analyste de performance digitale, Expert en commerce électronique, Spécialiste SEO/SEM, Community Manager, Conseiller en stratégie digitale, Responsable CRM, Spécialiste en Business Intelligence, Consultant en transformation digitale, Responsable des partenariats digitaux, Directeur de l’innovation digitale, Manager de l’e-réputation.<br>**ASI :** Auditeur des systèmes d’information, Consultant en sécurité des systèmes d’information, Analyste de risques IT, Chef de projet SI, Responsable de la conformité IT, Spécialiste en cyber forensics, Directeur de l’audit et de la sécurité des systèmes d’information, Expert en gouvernance IT, Formateur en sécurité IT, Chercheur en sécurité IT. |

## 1.8. Ressources humaines

Les ressources humaines sont citées ci-dessous selon leurs responsabilités :

- Directeur de l’École : Monsieur MAHATODY Thomas, Professeur ;
- Responsable de la mention « Informatique » : Monsieur RALAIVAO Jean Christian, Maître de Conférences ;
- Responsable de la mention « Intelligence Artificielle » : Monsieur DIMBISOA William Germain, Maître de Conférences.

L’ENI compte douze (12) enseignants permanents dont un (01) Professeur Titulaire, deux (02) Professeurs, sept (07) Maîtres de Conférences et deux (02) Assistants d’Enseignement Supérieur et de Recherche, ainsi que dix (10) enseignants vacataires et quarante et un (41) membres du personnel administratif.

@chapter Chapitre 2. Présentation de TETIKA

Ce chapitre présente l’entreprise TETIKA, société d’accueil dans le cadre de ce projet de fin d’études. TETIKA est aujourd’hui la société principale du groupe MANAO.

## 2.1. Information générale sur la société

La société TETIKA a son siège social à Ankadivory Ambohimiandra, Lot VP 26 Q – Immeuble KINTANA, Antananarivo 101 – Madagascar. Elle dispose également de bureaux secondaires à Toamasina et à Fianarantsoa, ainsi que d’un établissement en France, à Montpellier, assurant le lien avec les partenaires et clients internationaux.

### 2.1.1. Coordonnées pour la prise de contact avec l’entreprise

@tabcap Coordonnées de l’entreprise TETIKA
@colw 1.2,2.6,1.4
| Site | Adresse | Téléphone |
|---|---|---|
| **France (siège du groupe)** | 14 rue des Anoubles, 34070 Montpellier, France | +33 (0)4 69 66 59 52 |
| **Antananarivo (siège social)** | Lot VP 26 Q Immeuble KINTANA, Ankadivory Ambohimiandra, Antananarivo 101 | +261 (0)32 11 659 00 |
| **Fianarantsoa** | Lot 232AG/3602 Ankofafa Ambony, Fianarantsoa 301 | +261 (0)32 11 659 17<br>+261 (0)32 11 659 00 |

## 2.2. Missions et historique

### 2.2.1. Historique : de MANAO à TETIKA, « Grandir Ensemble »

Créée en 2008 à Montpellier, l’entreprise MANAO avait pour mission initiale le développement de logiciels de gestion en ligne. En 2013, elle s’est implantée à Antananarivo, puis s’est développée rapidement à Toamasina (2018) et à Fianarantsoa (2019). Au fil du temps, plusieurs entités spécialisées ont été créées :

- **Manao Logiciels :** édition de logiciels pour les entreprises et les établissements scolaires ;
- **TETIKA :** conseil et assistance en gestion ;
- **Ezaka :** externalisation administrative et BPO ;
- **Sidina :** développement web et mobile ;
- **Bambootech :** industrie et exportation de bambou.

En 2025, dans un objectif de simplification et d’efficacité, le groupe MANAO a fusionné ses principales activités sous la marque TETIKA, qui est désormais la société porteuse de l’ensemble des pôles (conseil, gestion, développement, formation). TETIKA perpétue la philosophie historique de MANAO : « Grandir Ensemble », en valorisant les compétences malgaches dans un contexte international.

### 2.2.2. Réussir à partir de Madagascar

Le projet du groupe d’entreprises est basé sur la réussite des collaborateurs malgaches. C’est parce que les collaborateurs de l’entreprise réussiront que l’entreprise réussira ; c’est parce que les Malgaches réussissent que le groupe réussit. L’ambition est d’avoir un groupe d’entreprises performantes, qui travaillent à l’international à partir de Madagascar : conquérir le monde à partir de Madagascar.

### 2.2.3. Valeurs : Confiance, Progression, Responsabilité

**Confiance.** Les collaborateurs se font mutuellement confiance, dans le travail comme dans le comportement. Aucune triche n’est tolérée : « 0 triche ».

**Progression.** Chacun a droit à l’erreur et doit s’en servir pour progresser, et faire progresser ses collaborateurs. La performance, l’exigence et l’expertise sont les éléments clés qui permettent de progresser jour après jour. Chacun doit être expert dans son domaine.

**Responsabilité.** Tout le monde n’est pas chef, mais chaque personne est responsable de ses tâches, de ses missions et des réalisations qu’elle effectue. On agit donc avec intelligence, en analysant le contexte, les situations et les conséquences de ce que l’on réalise. Les collaborateurs ne sont pas de simples exécutants : ils se doivent d’agir et d’être responsables.

## 2.3. Organigramme fonctionnel et hiérarchique de TETIKA

L’entreprise est sur le point d’entrer dans le stade de Petite et Moyenne Entreprise (PME), aussi l’organigramme commence-t-il à prendre forme. Dans l’optique de coordonner l’ensemble, des directions ont été mises en place, notamment une direction gestion et commerciale, avec à sa tête Monsieur Pascal AMET, et une direction technique et développement, coordonnée par Monsieur Guillaume VIGOUROUX.

L’organigramme, étant l’outil le plus utilisé pour schématiser une structure donnée, permet un aperçu global de l’ensemble. La figure 3 représente celui de TETIKA.

@img fig_bokyy/p015_n006.png | 1.0 | Organigramme fonctionnel et hiérarchique de l’entreprise TETIKA

Pour illustrer plus en détail la répartition des fonctions au sein de la direction technique et du développement, un organigramme spécifique est présenté dans la figure 4. Il met en évidence les équipes, les rôles et les responsabilités propres à ce service, dont l’équipe des tests automatisés au sein de laquelle s’inscrit ce travail.

@img fig_bokyy/p016_n008.png | 1.0 | Organigramme fonctionnel de la direction du développement

## 2.4. Domaines d’expertise

### 2.4.1. Compétences métiers

TETIKA dispose de compétences en gestion et en développement informatique, que ce soit auprès de TPE, de PME ou de grands groupes.

En gestion :

- comptabilité ;
- fiscalité ;
- social ;
- organisation en entreprise.

En développement informatique :

- développement d’applications de gestion (logiciels, sites e-commerce) ;
- développement web (PHP, HTML, Python, Java) ;
- développement mobile ;
- compétences sur des domaines connexes : bases de données, infrastructure serveurs, data center, hébergement, télécommunication, assistance, formation.

### 2.4.2. Branches et activités

Le groupe est divisé en branches, chacune correspondant à une activité :

- Manao Logiciels : www.manao.eu
- Sidina : www.sidina.eu
- TETIKA : www.tetika.eu
- Ezaka : www.ezaka.eu

## 2.5. Métiers

### 2.5.1. Métiers productifs

- Les développeurs ;
- les gestionnaires.

### 2.5.2. Services supports transversaux

- Les gestionnaires (DAF) ;
- la gestion du personnel et le recrutement ;
- les commerciaux ;
- les graphistes ;
- les techniciens d’assistance ;
- les techniciens système et réseau.

@chapter Chapitre 3. Description du projet

Ce chapitre décrit le projet afin de comprendre ce qui a été réalisé, pourquoi cette solution a été retenue, quels moyens ont été mobilisés et quels résultats sont attendus.

## 3.1. Formulation

Le projet porte sur l’étude de la mise en place de l’intégration et du déploiement continus d’une application en architecture microservices, combinée à l’orchestration des services déployés.

## 3.2. Objectif du projet

Les applications modernes basées sur des architectures microservices nécessitent une coordination efficace des différents services pour maintenir leur fiabilité et leur disponibilité.

Ce projet vise donc à concevoir et à mettre en œuvre un pipeline CI/CD et un mécanisme d’orchestration, afin d’automatiser le processus de livraison des microservices, de sécuriser les déploiements et de garantir une gestion fluide et évolutive des services.

## 3.3. Moyens nécessaires à la réalisation du projet

La réussite de ce projet repose sur la mise à disposition de ressources adaptées, tant humaines que matérielles et logicielles, permettant de concevoir, déployer et tester efficacement le pipeline CI/CD et l’orchestration des microservices.

### 3.3.1. Moyens humains

La réalisation de ce projet nécessite l’implication de profils disposant de compétences techniques variées. La coordination et la collaboration entre ces différents acteurs sont primordiales pour assurer la cohérence des déploiements, le respect des bonnes pratiques et la qualité globale du système. Les moyens humains sont présentés dans le tableau 6.

@tabcap Moyens humains nécessaires à la réalisation du projet
@colw 1.2,3.5
| Désignation | Rôle |
|---|---|
| **Développeurs** | Maîtrisent Node.js et Python ; développent et maintiennent les microservices. |
| **Ingénieur DevOps** | Conçoit et maintient le pipeline CI/CD, l’infrastructure et l’orchestration des services. |
| **Encadreurs** | Suivent l’évolution du travail, orientent les choix techniques et méthodologiques et valident la conformité du travail réalisé. |

### 3.3.2. Moyens matériels

Le projet requiert un environnement de développement et de déploiement virtualisé. Des serveurs virtuels hébergés sur une machine locale via VirtualBox et Vagrant sont utilisés afin de simuler l’environnement de production. Ces machines virtuelles permettent de tester le pipeline CI/CD, de déployer les microservices et de vérifier leur orchestration dans des conditions proches du réel. Une connexion Internet stable est également indispensable pour accéder aux plateformes de gestion de code, aux images Docker et aux outils distants.

@tabcap Moyens matériels nécessaires à la réalisation du projet
@colw 1.2,3.5
| Désignation | Caractéristiques |
|---|---|
| **Machine hôte** | Ordinateur capable d’héberger trois machines virtuelles (8 Go de RAM réservés au cluster) |
| **Machines virtuelles** | 1 nœud master (4 Go de RAM, 2 vCPU) et 2 nœuds workers (2 Go de RAM, 1 vCPU chacun) sous Ubuntu 20.04 LTS |
| **Connexion Internet** | Accès stable à GitHub, au registre d’images et aux dépôts de paquets |

### 3.3.3. Moyens logiciels

Plusieurs outils et technologies sont nécessaires afin de concevoir, automatiser et orchestrer efficacement l’ensemble des microservices et du pipeline CI/CD. Ils sont décrits dans le tableau 8.

@tabcap Moyens logiciels nécessaires à la réalisation du projet
@colw 1.2,3.5
| Outil | Utilité |
|---|---|
| **Git** | Assurer la gestion de versions et faciliter la collaboration entre les équipes |
| **Docker** | Conteneuriser les microservices et standardiser les environnements de développement et de déploiement |
| **Kubernetes** | Orchestrer les services et garantir la scalabilité et la haute disponibilité de l’application |
| **GitHub Actions** | Automatiser le pipeline CI/CD et les processus de build et de déploiement |
| **YAML** | Rédiger les scripts d’automatisation du pipeline et les manifests Kubernetes |
| **GraphQL** | Gérer la communication et l’échange de données entre les microservices |
| **Vagrant / VirtualBox** | Provisionner et exécuter les machines virtuelles du cluster |
| **Cypress** | Exécuter les tests automatisés de bout en bout après déploiement |

## 3.4. Résultats attendus

À terme, ce projet devrait permettre d’automatiser l’intégration et le déploiement des microservices via un pipeline CI/CD, garantissant ainsi une livraison rapide, fiable et cohérente des services tout en réduisant les risques d’erreurs liées aux interventions manuelles. Cette automatisation contribuera à améliorer la qualité globale des déploiements et à accélérer le cycle de vie des applications.

Par ailleurs, l’orchestration des services assurera leur scalabilité et leur haute disponibilité, permettant à l’application de fonctionner de manière continue, même en cas de charge importante ou de défaillance d’un service. La conteneurisation et la gestion centralisée des environnements via des outils comme Docker et Kubernetes faciliteront la maintenance, la portabilité et la standardisation des microservices.

## 3.5. Chronogramme de travail

Le diagramme de Gantt est un outil de planification qui permet de visualiser l’enchaînement des différentes tâches d’un projet. Il montre la durée prévue pour chaque étape et sa position dans le temps, ce qui facilite le suivi de l’avancement et l’organisation du travail. La réalisation de ce projet s’est déroulée sur une période de douze semaines, organisée en plusieurs phases distinctes présentées dans la figure 5.

@gantt

Pour clarifier la figure 5, le tableau 9 propose un récapitulatif des phases et de leur planification.

@tabcap Récapitulatif du chronogramme de travail
@colw 1.6,2.8,0.9,0.9
| Phase | Activités principales | Durée | Semaines |
|---|---|---|---|
| 1. Mise en place de l’infrastructure | Installation des serveurs virtuels, configuration des environnements de développement et de déploiement | 2 semaines | S1 – S2 |
| 2. Étude et conception du pipeline CI/CD | Définition des workflows, scripts d’automatisation, règles d’intégration et de déploiement continus | 3 semaines | S3 – S5 |
| 3. Déploiement de la première version de l’application | Intégration initiale des microservices, tests de fonctionnement du pipeline et de l’orchestration | 2 semaines | S6 – S7 |
| 4. Intégration et déploiement de nouvelles fonctionnalités | Déploiement des mises à jour dans les microservices existants, validation de la cohérence et de la stabilité | 3 semaines | S8 – S10 |
| 5. Tests post-déploiement et validation finale | Vérification de la fiabilité, de la scalabilité et de la performance globale, documentation des résultats | 2 semaines | S11 – S12 |
