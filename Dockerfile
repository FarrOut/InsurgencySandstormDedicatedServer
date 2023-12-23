FROM steamcmd/steamcmd:latest

WORKDIR /app

RUN steamcmd +login anonymous +force_install_dir /app +app_update 581330 validate +quit

COPY ./config/ /app/Insurgency/Saved/Config/LinuxServer/
COPY ./mods/ /app/Insurgency/Mods/

EXPOSE 27102/udp
EXPOSE 27131/udp

CMD ["/app/Insurgency/Binaries/Linux/InsurgencyServer-Linux-Shipping", "Insurgency?Scenario=Scenario_Checkpoint_Security?MaxPlayers=8?Port=27102?QueryPort=27131?AdminList=Admins.txt"]
