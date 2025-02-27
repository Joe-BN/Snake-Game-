# Snake-Game-

![nvimscreen](https://github.com/Joe-BN/Nvim/assets/128038111/597f8228-4669-4736-9860-76d00c19e296)

Using [lazy.nvim](https://github.com/folke/lazy.nvim) to bring in some useful functionality without making it too complex.

Features include:
+ Base player (player 01): just like any other snake game
+ Difficulty levels (easy, medium, hard and Asian 😂)
+ High score storage in a database (mighty convenient)


+ ✨ Multiplayer ! 💎✨

  
(All configured in code to be easy to modify)




For those new to this:

+ 1st, Install Neovim & git with the package manager of your choice ( mine is pacman, coz I use Arch btw :) ):

```
$ sudo pacman -S neovim
```

and

```
$ sudo pacman -S git
```

+ 2nd, Create the ```nvim/``` folder in your ```.config/``` folder
+ 3rd, ``` cd ``` into ``` ~/.config/nvim ``` and clone the code from my repo from within with:
```
$ git clone https://github.com/Joe-BN/Nvim/config
```

-> Run the following command to unpack all the necessary files into the current directory

```
$ mv Nvim/config/* .
```

-> Run this to delete the ``` Nvim ``` folder gotten from github:
``` 
$ rm -rf Nvim
```

-> When you run ```$ tree nvim``` while inside the ```.config/``` directory, it should display this:

![nvimtree2](https://github.com/Joe-BN/Nvim/assets/128038111/17d26f0c-f854-4e02-a25a-3d9ed3517b32)

-> After the setup above, run ```$ nvim ``` and Lazy will download and sync the required dependencies.

Enjoy     : )
