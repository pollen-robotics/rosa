[![Build Status](https://travis-ci.org/pollen-robotics/rosa.svg?branch=master)](https://travis-ci.org/pollen-robotics/rosa)

# Le projet Rosa : un robot ramasseur d'objets

Le robot Rosa a été conçu dans le cadre d'une mission de [Poppy station](https://www.poppystation.org) effectuée par [Pollen-Robotics](https://www.pollen-robotics.com) et visant à concevoir un robot pour l'éducation capable de se déplacer dans l'environnement, de détecter et reconnaître des objets et de les transporter. Il peut être programmé depuis un ordinateur ou une tablette en Python ou Scratch 3.

Ce projet est entièrement open-source et s'appuie sur des composants Makers et DIY. Il a été conçu pour être facilement assemblable et personalisable. Il vise à être construit et distribué par les réseaux de distribution de la ligue pour l'Enseignement.

**TODO: video**

## Guide de démarrage

### Les différents modèles 3D et composants
### Assemblage

### Préparer la carte SD

Le logiciel embarqué du robot est disponible sous forme ISO prête à flasher sur une carte SD (8Go minimum). Cette ISO est disponible [ici](TODO). Ce logiciel est responsable de piloter les moteurs en fonction des commandes reçues ainsi que d'envoyer les informations des différents capteurs.

Pour plus d'information sur comment écrire cette image on pourra se référer, par exemple, au site de Raspberry Pi [à cette adresse](https://www.raspberrypi.org/documentation/installation/installing-images/README.md).

Une fois la carte écrite avec l'image téléchargée, elle peut être insérée dans la carte Raspberry Pi de Rosa.

Afin de simplifier la première connexion au réseau WiFi, il est possible de le paramétrer directement sur la carte SD que l'on vient d'écrire. Il peut donc être plus pratique de réaliser cette étape avant d'insérer dans le robot (voir section [Connecter au réseau WiFi](#wifi) pour plus d'informations).

### Alimentation

### Connecter Rosa au réseau

Afin de pouvoir programmer le robot, il est nécessaire de le connecter au même réseau que son ordinateur ou sa tablette. Il peut se connecter au WiFi ou en Ethernet via un adaptateur USB.

#### WiFi

La carte Raspberry-Pi utilisée par le robot permet de se connecter à un réseau WiFi. Il est donc possible de la configurer comme n'importe quelle carte Raspberry-Pi.

Si vous avez facilement accès à la carte, il est possible de brancher un clavier (en USB) et un écran (en HDMI) sur la carte et d'utiliser l'interface graphique de Raspberry-Pi pour configurer un réseau WiFi. Ce réseau sera conservé et le robot utilisera automatiquement ce réseau.

Il est également possible de venir rajouter un fichier spécial directement sur la partition BOOT de la carte SD. Par exemple, si on souhaite se connecter automatiquement au réseau WiFI "mon-reseau-wifi" avec comme mot de passe "password" il faut ajouter le fichier *wpa_supplicant.conf* suivant :

```
country=fr
update_config=1
ctrl_interface=/var/run/wpa_supplicant

network={
    ssid="mon-reseau-wifi"
    psk="password"
}
```

Plus d'informations sur comment connecter une Raspberry-Pi à un réseau WiFi sont disponibles [sur le site de Raspberry-Pi](https://www.raspberrypi.org/documentation/configuration/wireless/).

#### Ethernet via USB

Il est également possible de connecter le robot au réseau via un cable en utilisant un adaptateur USB-Ethernet et en utilisant le port USB accessible à l'arrière du robot.

La détection du réseau est alors automatique.

#### Utilisation de ZeroConf

Le robot est toujours accessible sur le réseau à l'adresse *rosa.local*. Cela permet de simplifier la procédure de connexion, il n'est pas nécessaire de connaître l'adresse IP du robot. Cette addresse est utilisée par défaut par l'extension Scratch 3.

Cependant, pour pouvoir fonctionner ZeroConf nécessite d'installer un logiciel sur l'ordinateur.

- Pour Windows : [Bonjour print services](https://support.apple.com/kb/DL999)
- Pour Linux : avahi-daemon (mDNS) et avahi-autoipd (IPv4LL)
- Pour MacOS : ZeroConf est déjà installé.

## Capacités et caractéristiques

Le robot a été conçu pour pouvoir être utilisé dans différentes activités et dans des contextes variés. Les différentes capacités et caractéristiques du robot sont présentées ci-dessous.

### Navigation

Le robot possède deux roues actionnées chacune par un moteur. Elles peuvent tourner vers l'avant, vers l'arrière et s'arrêter. Le robot est donc capable de se déplacer dans un plan et de tourner sur lui même. La vitesse de déplacement du robot est réglable (**TODO: fourchette**).

### Détection d'obstacles

Le robot possède plusieurs capteurs de distance (utilisant un émetteur/récepteur infra-rouge). Ces capteurs sont situés à l'avant du robot ainsi que sous le robot.

Ceux situés à l'avant peuvent être utilisés pour faire de la détection d'obstacles ou suivre un objet. Ils détectent un objet situé à une distance de 5 à 15cm. Ils permettent de mesurer la distance. Les capteurs sont positionnés :

- à l'avant gauche
- à l'avant centre
- et à l'avant droite.

À noter que le capteur central peut également être utilisé pour mesurer la couleur d'un objet positionné juste devant.

Ceux situés sous le robot sont utilisés pour détecter le vide, par exemple un bord de table. Ils peuvent également servir à détecter une ligne noire si elle est suffisament large (~ la largeur du robot). Il y a 4 capteurs de bord de table situés à chacun des coins du robot.

### Suivi de ligne

Le robot peut également suivre une ligne noire. La caméra est utilisée pour la détecter et identifier sa position verticale à une distance du robot donnée.

**TODO: vidéo et images**

### Détection et reconnaissance d'objet

Le robot peut également détecter et reconnaître certains objets placés devant lui. Cette capacité permet la création d'activités autour de la collecte, du convoyage et du tri d'objets.

Les objets de couleur reconnus par le robot sont un cube, une étoile et une boule. Le modèle 3D de ces objets est disponible [ici](**TODO**) et ils sont facilement imprimables sur une imprimante 3D du commerce.

La caméra du robot est utilisée pour reconnaître et détecter ses objets. Le robot renvoie une liste de l'ensemble des objets présents à l'image (il n'y a pas de limite maximale) avec pour chacun des objets son type (cube, étoile ou boule) et sa position dans l'image (la boite englobante).

**TODO: video + image**

*Note: il est possible, bien que plus compliqué, d'entrainer le robot à reconnaître de nouveaux objets si l'on souhaite.*

### Autres interactions

Le robot est également équipé d'un buzzer et de deux leds à l'avant permettant d'enrichir les interactions possibles.

## Utilisation

### Python

L'API Python permet de controler le robot, d'accéder aux valeurs renvoyées par les senseurs ainsi que d'accéder à la caméra. Elle permet également l'utilisation des primitives de vision telles que la détection d'une ligne noire ou la détection d'objets.

Pour plus de détails, se reporter à la documentation dédiée : [Python's API](./api/python/readme.md)

### Scratch 3

Le robot peut également être programmé à l'aide d'une version dédiée de Scratch 3. Elle est accessible en ligne directement ici : http://www.scratch.pollen-robotics.cc

Les différents blocs proposés sont présentés ici : [extension Rosa pour Scratch 3](./api/scratch/readme.md).
