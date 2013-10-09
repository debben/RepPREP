RepPREP
=========
RepPREP (Pi-bassed RepRap Expansion Platform) aims to be a web-bassed equivalent of [ReplicatorG]. From the browser, you can manage machine settings, Skeinforge profiles, and print parts. The goal is that all the work is done on the server side, so you can potentially print things from devices like Chromebooks, tablets, and smartphones. 

RepPREP can potentially be used to manage and run several printers at the same time and even manage use accross many users. It forms the basis for what you need to run a networked-print farm. My initial idea was to just be able to add a Raspberry Pi to any 3d printer to give it networked functionality.

Compatibility
-------------
At this time, RepPREP is designed for use with 3d printers using the S3G protocol (makerbot/reprap motherboard gen3+). This is thanks to a [Python implementation] of the S3G protocol. If you RepPREP to speak something else, just fork and shoot me a pull request. I'm very open to sugestions for how to grow RepPREP.

Notes
------
This is my first attempt at writting a Django app. It's also been many years since doing anthing big in Python. As such, there are probably some naming/casing conventions and other best practices I'm trampling on. If it bugs you enough, just send me a patch. I'll be refactoring as I learn more about Django but right now I'm just focusing on getting the core functionallity online.

Installation
--------------
At this time, I don't have any install instructions. When I start moving development onto a fresh install of Linux on my laptop, I'll keep track of any system dependancies that are missing and wrap it up into a script. 

License
----
GPLv3

  [ReplicatorG]: https://github.com/makerbot/ReplicatorG
  [Python implementation]: https://github.com/makerbot/s3g
  
    