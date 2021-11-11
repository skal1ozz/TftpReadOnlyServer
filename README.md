# TftpReadOnlyServer
###A handy wrapper for the py3tftp server that makes the server read only. 
For those who don't wanna spend time on hacking it or looking for a read only servers out there.

#### How to install:

1. Download this project:

        # Create working directories
        mkdir -p ~/Projects/python/

        # Open it
        cd ~/Projects/python/

        # Clone the project
        git clone https://github.com/skal1ozz/TftpReadOnlyServer

2. Create a virtual environment:

        # Open project dir
        cd ~/Projects/python/TftpReadOnlyServer

        # Make a virtual environment
        python -m venv .venv

3. Install requirements.

        # Activate venv
        source .venv/bin/activate

        # Install requirements
        pip install -r requirements.txt

####How to run:

1. Create a working directory for the server:

        # This is a directory where you should put your files to share
        mkdir -p /tmp/tftpboot/

2. Start the server:

        # Go to working directory
        cd /tmp/tftpboot/

        # Reactivate your venv if you've had deactivated it. 
        source ~/Projects/python/TftpReadOnlyServer/.venv/bin/activate

        # Start the server
        python ~/Projects/python/TftpReadOnlyServer/tftp.py --port 69

    You should see these lines if everything went well:

        2021-11-11 23:32:06,250 [INFO] Starting TFTP server on 0.0.0.0:69
        2021-11-11 23:32:06,251 [INFO] Listening...


####What's next?

You can create a systemd service and install this server as a service

Here's an example:

    # Creating a service file

    # get your home dir path
    cd ~
    HOME_DIR=$(pwd)
    echo "your home dir is: $HOME_DIR"
    
    cat << EOF > ~/Projects/python/TftpReadOnlyServer/tftp-server.service
    [Unit]
    Description=TFTP Server
    After=network.target
    
    
    [Service]
    Type=simple
    Restart=always
    RestartSec=1
    User=root
    WorkingDirectory=/tmp/tftpboot/
    ExecStart=$HOME_DIR/Projects/python/TftpReadOnlyServer/.venv/bin/python \\
              $HOME_DIR/Projects/python/TftpReadOnlyServer/tftp.py --port 69
    
    [Install]
    WantedBy=multi-user.target
    EOF
    
    # Install your service
    cp ~/Projects/python/TftpReadOnlyServer/tftp-server.service /etc/systemd/system/
    
    # Enable your service
    systemctl enable tftp-server

    # And finally start your service
    systemctl start tftp-server

Now if everything went well you can check your serve with the command:

    systemctl status tftp-server

You should see something lile this:

    ● tftp-server.service - TFTP Server
       Loaded: loaded (/etc/systemd/system/tftp-server.service; enabled; vendor preset: enabled)
       Active: active (running) since Fri 2021-05-14 00:53:17 UTC; 5 months 29 days ago
     Main PID: 13017 (python)
        Tasks: 1 (limit: 2322)
       CGroup: /system.slice/tftp-server.service
               └─13017 /home/demo/Projects/python/TftpReadOnlyServer/.venv/bin/python /home/demo/Projects/python/TftpReadOnlyServer/tftp.py --port 69

####How to test?

1. Open your tftp working directory and create a test file

        # Make a test file
        cat << EOF > /tmp/tftpboot/greetings.txt
        Hello world
        EOF

2. Download the file

        # Change directory (your might be in /tmp/tftpboot/)
        cd ~/Projects/python/TftpReadOnlyServer/
        
        # Download your file
        tftp 127.0.0.1 << EOF
        get greetings.txt
        EOF

If everything went well you should see something like this:

    Received 38 bytes in 0.0 seconds

You can browse your directory

    cd ~/Projects/python/TftpReadOnlyServer/
    ls -l

And you should see `greetings.txt` in your directory:

    total 48
    -rw-r--r--  1 demo  staff  1066 Nov 11 23:03 LICENSE
    -rw-r--r--  1 demo  staff  3996 Nov 12 00:20 README.md
    -rw-r--r--  1 demo  staff    34 Nov 12 00:14 greetings.txt
    -rw-r--r--  1 demo  staff    15 Nov 11 23:15 requirements.txt
    -rwxr-xr-x  1 demo  staff  1927 Nov 11 23:04 tftp.py
