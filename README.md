![logo](https://bitbucket.org/millesroom/3_semester/raw/dd438d352f38ae24e7e02eb2deb89c59f64dfef1/img/img.png)

# Hvorfor:
Formål med virksomheden er at øge sikkerhed for outdoor aktivitets udøvere i tilfælde af nødsituationer. Designet skal gøre det nemmere for redningsfolk at få den præcise lokationen for nødlidende. 
# Hvordan: 
Designe tøj til vandring, skiløb, klatring og sejlads, med en indbygget IoT enhed som nemt kan aktiveres og udsende geolokation til alarmcentral. Ved aktivering vil der også være en sensor som registrerer temperatur, som sendes i tidsinterval indtil redningsfolkene er ankommet. 
# Hvad: 
Brandet hedder ResQWear og logoet har SOS-nødsignal med lokation som symbol. Logoet viser funktionen i tøjdesignet

# Refleksioner:
Enheden skal manuelt aktiveres inden paabegyndt aktivitet, paa den maade sikres brugeren ikke at blive uoensket tracket 

Mulighed for en "last known position" funktion, hvor timestamp/coords sendes kontinuerligt hver time og kan tilgaaes ved mistanke om vedkommende er faret vild, kommet til skade mm. men ikke har aktiveret et alarmsignal. 

Mulighed for at sende "connected" beskeder, uden en aktiveret alarm. Dette er for at sikre at enheden er pre-aktivieret og funktionel, men der ikke er sendt alarmsignal. 

<hr>

# udp test
Bruges til kontinuerlige "conencted"-beskeder, for at paavise om enheden er funktionel, og for at kunne logge timestamp/coords i tilfaelde af at der er brug for "last known position".

![logo](https://bitbucket.org/millesroom/3_semester/raw/4fede365c66a6b17df5debde3ed22651daddabef/img/Screenshot%20udpTest%202025-10-21%20131833.png)

# tcp test 
Denne forbindelse er til det aktiverede alarmsignal som skal sendes sikkert, da der er sket en noedsituation og redningsfolk skal tilkaldes. 

![logo](https://bitbucket.org/millesroom/3_semester/raw/14c526bf71a1a20ec8d356532d6d5d3dba46e593/img/Screenshot%20tcpclient%202025-10-21%20103735.png)

# iridium test
Iridium er satellit system til forbindelse mellem enhed og internet/cellular i fjernliggende egne. Server/Client/Test skal tilpasses projektet, dette er midlertidig dokummentation af succesful kommunikation med koder skrevet af ChatGPT

"test_invalid_connection PASSED
Den test, der sender “bad data”, er også bestået. Formålet med testen er at sikre, at serveren ikke crasher, selv når den modtager noget, der ikke ligner en rigtig SBD-pakke.

[INFO] Connection from ('127.0.0.1', 39713)
En testklient oprettede forbindelse til serveren.

[DEBUG] Received 8 bytes ... b'6261642064617461'
Her ser du, at serveren modtog 8 bytes.
De bytes svarer til teksten "bad data" i hex:

62 61 64 20 64 61 74 61 = "bad data"
Altså den forventede “dårlige” testbesked.

[WARN] Not a valid SBD MO request (wrong header byte).
Serveren kontrollerede første byte (header), som i SBD-format skal være 0x01,
men her var det 0x62 (bogstavet b), så serveren reagerede korrekt med en advarsel.
Den crashede ikke, hvilket var hele pointen med testen.

[INFO] Server stopped.
Pytest-fixture lukkede serveren rent, efter testen var færdig.
" ChatGPT
![logo](https://bitbucket.org/millesroom/3_semester/raw/d5e96a02996da0fef97eb32ba4e5ba567c2ba085/img/iridium%20test%202025-10-23%20102629.png)

Emergency test

![logo](https://bitbucket.org/millesroom/3_semester/raw/aeaafb34c7fbc55a7af8c36fff77ffd0c3c65b47/img/Iridium%20emergency%202025-10-28%20130946.png)

Last known position test

![logo](https://bitbucket.org/millesroom/3_semester/raw/aeaafb34c7fbc55a7af8c36fff77ffd0c3c65b47/img/Iridium%20lkp%202025-10-28%20131056.png)

# Fysisk forbindelser
Denne enhed skal kunne kommunikere fra fjerntliggende lokationer, det betyder at cellular og WiFi forbindelser er udelukket, det samme er LoRa da raekkevidden ikke er tilstraekkelig. Forbindelsen skal derfor vaere Satellitlink. 
ChatGPT har praesenteret Iridium som en mulighed. Jeg har ogsaa diskuteret brug af Starlink. Forskellen paa Iridium og Starlink er blandt andet at Starlink bruger mere stroem, haandterer stoerre datamaengder og kraever stoerre hardware (antene). Hvor imod Iridium er god til smaa datamaengder (se hjemmeside for praecis datamaengde men omkring 340 bytes ud), hardwaren er mindre og kompakt hvilket er noedvendigt for funktionaliteten. 

Iridium er et system af 66 internt forbundene, intern-satellite links, satelitter LEO -Low Earth Orbit, som enheden forbinder til, satelitten forbinder til en Gateway paa jorden, som forbinder til internet/cellular. 

# Budget og ressource overvejelser 
Iridium er relativt dyr og abonnomentbaseret, hvilket jeg ikke mener egner sig til et skoleprojekt. Derfor vil jeg i dette projekt udarbejde en teoretisk loesning som kan testes og bevises. Til dette vil jeg bruge UDP og TCP client/server og en Raspberry Pi  med WiFi som mikrocontroller. 

Jeg vil redegoere for faglige overvejelser for at bruge Iridium (in real life), hvordan det skulle integreres i projektet, og egentligt goere det "ready for production". Paa den maade bliver dette projekt to-delt. 

Dette er mine umildbare tanker i forhold til ressourcemaessig afgraensing af projektet. 

# API
![logo](https://bitbucket.org/millesroom/3_semester/raw/97efd65c8c0513d49b561de82b2c174f9f531e73/img/Screenshot%20api%202025-10-30%20113855.png)

curl api: 127.0.0.1 - - [30/Oct/2025 11:47:29] "GET /api/health HTTP/1.1" 200 -

![logo](https://bitbucket.org/millesroom/3_semester/raw/6c9d1aa386d3b87ef6ff5fc75293310bb6d7e500/img/curl_api%202025-10-30%20114754.png)