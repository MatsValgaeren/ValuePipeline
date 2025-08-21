# ValuePipeline

### My own VFX Pipeline for Post-Production, WIP

<details>
<summary>Table of Contents</summary>

- [About](#about)
- [Foreword](#forward)
- [Hardware](#hardware)
- [Credits](#credits)
- [License](#license)

</details>

## about

This project is meant as a way for me to show of what I am working on and for archiving/git control for myself. These scripts are not meant for deployment for other people, although you could take inspiration from this. You could also accidentally share this with all your nerd friends or slide a job offer in my mail: contact@matsvalgaeren.com .

##  Foreword

I aspire to become a Pipeline TD and I felt like I missed quit a bit of programming/ computer knowledge. So what better way to learn more about pipelines then to TRY to build my own so I could make some Marvel quality movies (Pre-EndGame).

The hardware I am using is not the best in any way. Each software or plugin I chose was at that moment the best fit. And I tried to make the best scrips possible with my limited knowledge. But it gets the job done pretty well and I am looking forward to using it in my next project.


## Hardware

The device running the actual pipeline is a 8GB Raspberry Pi 5 with a Radxa sata hat that holds 2 hard drives I harvested from old laptops from my parents. I am running Pi OS Lite on it for extra performance. I also have OpenMediaVault installed because it makes managing the services easier for a noob like me. I am familiar with it from running it on my home media server. The drives are setup with SnapRaid and MergeFS, this probably doesn't change the performance a lot but it gives me the right to add some more cool words in this paragraph.

The 'render node' is my old desktop that I had abandoned when I bought a laptop for school. It has a Ryzen 3 3300x and a RTX 3060 is running Rocky 10 Minimal. I am also using rocky as one of my boot options on my laptop and I want to get more used to this distro because it is recommender by the VES. I do not have access to a router where I have installed these systems, so I am sharing the WiFi connection from the Pi to this device. The Pi is also setup to shutdown and wake this device over LAN.

My laptop is my workstation where I program the scripts and ssh into the other devices to control them like a telekinetic. All these devices are connected with a basic switch and static local IPs. Uploading/ rendering files is possible locally, or remotely by using the WireGuard VPN. I am not planning to open the program up to the internet because I have no idea how to safely do this without getting my nudes leaked.



## Credits

-   Script by Mats Valgaeren

## License

[GNU General Public License v3.0](LICENSE)
