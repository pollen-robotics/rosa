# Le projet Rosa : un robot ramasseur d'objets

Le robot Rosa a été conçu dans le cadre d'une mission [Poppy station](https://www.poppystation.org) effectuée par [Pollen-Robotics](https://www.pollen-robotics.com) et visant à concevoir un robot capable de se déplacer dans l'environnement, de détecter et reconnaître des objets et de les transporter. Il peut être programmé depuis un ordinateur ou une tablette en Python ou Scratch 3.

Ce projet est entièrement open-source et s'appuie sur des composants Makers et DIY. Il a été conçu pour être facilement assemblable et personalisable. Il vise à être construit et distribué par les réseaux de distribution de la ligue pour l'Enseignement.

**TODO: video**

## Guide de démarrage

### Les différents modèles 3D et composants
### Assemblage

### Préparer la carte SD

Le logiciel embarqué du robot est disponible sous forme ISO prête à flasher sur une carte SD (8Go minimum). Cette ISO est disponible ici : [TODO](TODO). Ce logiciel est responsable de piloter les moteurs en fonction des commandes reçues ainsi que d'envoyer les informations des différents capteurs.

Pour plus d'information pour écrire cette image est, par exemple, accessible sur le site de Raspberry Pi [à cette adresse](https://www.raspberrypi.org/documentation/installation/installing-images/README.md).

Une fois la carte écrite avec l'image téléchargée, elle peut être insérée dans la carte Raspberry Pi de Rosa.

Afin de simplifier la première connexion au réseau WiFi, il est possible de le paramétrer directement sur la carte SD que l'on vient d'écrire. Il peut donc être plus pratique de réaliser cette étape avant d'insérer dans le robot (voir section [Connecter au réseau WiFi](#wifi) pour plus d'informations).

### Alimentation

### Connecter Rosa au réseau

Afin de pouvoir programmer le robot, il est nécessaire de le connecter au même réseau que son ordinateur ou sa tablette. Il peut se connecter au WiFi ou en Ethernet via USB.

#### WiFi

La carte Raspberry-Pi utilisée par le robot permet de se connecter à un réseau WiFi. Il est donc possible de la configurer comme n'importe quelle carte Raspberry-Pi.

Si vous avez facilement accès à la carte, il est possible de brancher un clavier (en USB) et un écran (en HDMI) sur la carte et d'utiliser l'interface graphique de Raspberry-Pi pour configurer un réseau WiFi. Ce réseau sera conservé et le robot utilisera automatiquement ce réseau.

Il est également possible de venir rajouter un fichier spécial directement sur la partition BOOT de la carte SD. Par exemple, si on souhaite se connecter automatiquement au réseau WiFI "mon-reseau-wifi" avec comme mot de passe "password" il faut ajouter le fichier wpa_supplicant.conf suivant :

```
country=fr
update_config=1
ctrl_interface=/var/run/wpa_supplicant

network={
    ssid="mon-reseau-wifi"
    psk="password"
}
```

Plus d'informations sur comment connecter une Raspberry-Pi à un réseau WiFi est disponible [sur le site de Raspberry-Pi](https://www.raspberrypi.org/documentation/configuration/wireless/).

#### Ethernet via USB

Il est également possible de connecter le robot au réseau via un cable en utilisant un adaptateur USB-Ethernet et en utilisant le port USB accessible à l'arrière du robot.

La détection du réseau est alors automatique.

## Capacités et caractéristiques

### Navigation
### Détection d'obstacles
### Suivi de ligne
### Détection et reconnaissance d'objet

## Utilisation

### Python
### Scratch 3
