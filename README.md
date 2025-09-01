# ValuePipeline

### My VFX Pipeline Project for Post-Production, WIP

<details>
<summary>Table of Contents</summary>

- [About](#about)
- [Foreword](#foreword)
- [Hardware](#hardware)
- [Scripts](#scripts)
- [Credits](#credits)
- [License](#license)

</details>

## About

This project is meant as a way for me to show of what I am working on and for archiving/git control for myself. These scripts are not meant for deployment for other people, although you could take inspiration from this. You could also accidentally share this with all your nerd friends or slide a job offer in my [mail](contact@matsvalgaeren.com).

![vp_flowdiagram_v001](https://github.com/MatsValgaeren/ValuePipeline/blob/main/assets/images/vp_flowdiagram_v001.png)

##  Foreword

I aspire to become a Pipeline TD and wanted to learn more by doing. So what better way to learn more about pipelines then to TRY to build my own so I could make some Marvel quality movies (Pre-EndGame).

## Hardware

The device running the actual pipeline is a 8GB Raspberry Pi 5 with a Radxa sata hat that holds 2 hard drives I harvested from old laptops from my parents. I installed [OpenMediaVault](https://www.openmediavault.org/) on top of [Pi OS](https://www.raspberrypi.com/software/) Lite because it makes managing the services easier for a noob like me. I am familiar with it from running it on my home media server. The drives are setup with [SnapRaid](https://github.com/amadvance/snapraid) and [MergeFS](https://github.com/trapexit/mergerfs), this probably doesn't change the performance a lot but it gives me the right to add some more cool words in this paragraph.

The 'render node' is my old desktop that I had abandoned when I bought a laptop for school. It has a Ryzen 3 3300x and a RTX 3060 is running Rocky 10 Minimal. I am also using rocky as one of my boot options on my laptop and I want to get more used to this distro because it is recommender by the [VES](https://vfxplatform.com/). I do not have access to a router where I have installed these systems, so I am sharing the WiFi connection from the Pi to this device. The Pi is also setup to shutdown and wake this device over LAN.

My laptop is my workstation where I program the scripts and ssh into the other devices to control them like a telekinetic. All these devices are connected with a basic switch and static local IPs. Uploading/ rendering files is possible locally, or remotely by using the WireGuard VPN. I am not planning to open the program up to the internet because I have no idea how to safely do this without getting my nudes leaked.

## Scripts

The Server/ NAS is running a [Flask](https://flask.palletsprojects.com/en/stable/) website where users can upload files in the [Dropzone](https://www.dropzone.dev/). These will then get proccesed, which entails downloading the file on the server and trying to get as much data out that can be used when saving the file in the database. This mostly means file name and trying to get the project/ task or version if named with a predefiened filename structure. For image files it will try to use exif data if it exists.

These uploaded files will shown to the user as processed, here he can chose to delete files from uploading. He also needs to fill in his name so we can track who uploaded it. He also has the option to render files if the render software exists on the Render Computer. The server is running a [Redis Queue](https://redis.io/glossary/redis-queue/) where files can be queued to be rendered. When he then choses to upload, all files will be uploaded to the upload folder, put in the [SQLite](https://sqlite.org/) database and rendered if needed, the process then resets. The server will shutdown the Render Computer when it has been empty for long, it will start the Render Computer when something is queued.

The Render Computer is running a Render tasks script which checks the queue and will render the tasks that it sees one by one. These will then get put in in a rendered folder on the NAS.

The database is currently pretty useless because I am using it nowhere, but I am planning to add a history to the site so you can see and search for previous uploads.

## Credits

-   Scripts by Mats Valgaeren

## License

[GNU General Public License v3.0](LICENSE)
