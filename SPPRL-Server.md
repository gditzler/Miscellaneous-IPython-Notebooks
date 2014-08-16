# About 

The server located in the [SPPRL](http://users.rowan.edu/~polikar/RESEARCH/SPPRL/) is in place for students to use more powerful computing resources than traditional PC or  high-end laptops. The software install of the server is tailored towards research in machine learning, data science, and optimization. The current server configuration can be summarized as: 

* 2 x Intel Xeon E5645 Six-Core 2.4GHz, 12MB Cache, 5.86GT/s QPI, 80W, 32nm
* 72GB (18 x 4GB) Operating at 800MHz Max (DDR3-1333 ECC Registered DIMMs)
* 3TB usable in a 6 drive Software RAID 10 array
* [OpenSuSe](http://www.opensuse.org/en/) (for the moment). The plan is to switch to [Debian](https://www.debian.org/)

Our future plan is to switch from OpenSuSe to Debian for ease of use, easier package management, and Debian is more familiar to students. 

## Installed Software

* Matlab
* Python: numpy, scipy, sklearn, pyfeast, pandas, qiime, matplotlib, IPython, ...
* R

# Getting Started

## Setting Up SSH Keys

Let us start out by setting up our SSH keys. Do this will avoid the need for you to have to enter your password every time you connect to the server, and you can follow these instructions to setup you SSH keys on GitHub. Again, going so would avoid the need to enter your password each time you push to one of your repositories. I shall assume that you are working on a Mac, Unix, or Linux terminal. Refer to the [Putty](http://www.chiark.greenend.org.uk/~sgtatham/putty/) documentation. 


First, check to see if you already have an SSH key(s). If you already have the files `id_rsa` and `id_rsa.pub` than you can jump forward a few steps. 
```bash
ls -la ~/.ssh
# Lists the files in your .ssh directory, if they exist
```

Next generate a new SSH with the command below. Note that you must replace the email with your email address. You will be prompted to enter  password for you new SSH key; however, you do not need to enter a new password if you do not want to (some will tell you this is a [bad idea](https://help.github.com/articles/working-with-ssh-key-passphrases)). 
```bash
ssh-keygen -t rsa -C "your_email@example.com"
# Creates a new ssh key, using the provided email as a label
```
Now you have a new SSH key in the `~/.ssh/` folder. Then add your new key to the ssh-agent, which is a nice tool to handle the passphrase, so you don't have to re-enter it. I think this does not need to be done for Mac because you can add the key into the [Keychain](http://en.wikipedia.org/wiki/Keychain_(Apple)). 
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
```
Next you want to copy your new SSH key to the server. 
```bash
cat ~/.ssh/id_rsa.pub | ssh {user}@{spprlserver ip address} "cat - >> ~/.ssh/authorized_keys"
```
where you must replace everything inside {.}  with the appropriate values.  Now that the SSH key is on the server, let us configure them so we can have a speedy login. Create a new file in the `~/.ssh/` folder named `config` (this can be achieved with the command `touch ~/.ssh/config`). Then using your favorite text editor modify the file to look like: 
```
Host spprl
  User Your_User_Name
  HostName SPPRL_IP_ADDRESS
```
where you will need to replace the fields in `User` and `HostName` (I have called the server `spprl` for convenience though you can name it what you want). Feel free to add as many new `Hosts` as you need.

SSHing into the server is as easy as
```bash
ssh spprl
# you no longer need to enter the password to the spprl server!
```

You can run 
```
pbcopy < ~/.ssh/id_rsa.pub
```
to copy the contents of your public key to the clipboard. Then add the SSH key to your GitHub account. Viola! No more remembering passwords.

## Setting Up Local Stuff

Create a local folder for binary files and add the folder to your `$PATH` variable. You should do this if you need to install software that the administrator is not going to install on the server globally. 
```bash
mkdir ~/.local
mkdir ~/.local/bin
touch ~/.bashrc
echo "#!/usr/bin/env bash" >> ~/.bashrc
echo "export PATH=$HOME/.local/bin/:$PATH" >> ~/.bashrc
```

## Transferring Data To/From the Server

You can transfer data to and from the server via the terminal, but its a hassle an no one has time for that. You should install a FTP (capable of providing a secure shell) client. Usuaully transfering data with one of these clients is as easy as dragging and dropping files to/from the server and local machine where the client is running. The best client that I know of is [Filezilla](https://filezilla-project.org/).
