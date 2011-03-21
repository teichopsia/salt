'''
Specilized routines used by the butter cloud component
'''
# Import salt modules
import virt

# Import python modules
import os
import shutil
import hashlib
import random

def _place_image(image, vda):
    '''
    Moves the image file from the image pool into the final destination.
    '''
    image_d = image + '.d'
    if not os.path.isdir(image_d):
        # No available images in the pool, copying fresh image
        shutil.copy(image, vda)
        return
    images = os.listdir(image_d)
    if not images:
        # No available images in the pool, copying fresh image
        shutil.copy(image, vda)
        return
    shutil.move(os.path.join(image_d, images[0]), vda)

def _gen_pin_drives(local_path, pin):
    '''
    Set up the pin drives called for in the creation of a new vm
    '''

def _apply_overlay(vda, overlay):
    '''
    Sets up the overlay on the passed vda
    '''
    if not os.path.isdir(overlay):
        return False
    instance = os.path.dirname(overlay)
    tarball = os.path.join(instance,
        str(hashlib.md5(str(random.randint(1000000,9999999))) + '.tgz')
    cwd = os.getcwd()
    os.chdir(overlay)
    t_cmd = 'tar czf ' + tarball + ' *'
    subprocess.call(t_cmd, shell=True)
    g_cmd = 'guestfish -i -a ' + vda + ' tgz-in ' + tarball + ' /'
    subprocess.call(g_cmd, shell=True)
    os.remove(tarball)
    os.chdir(cwd)

def local_images(local_path):
    '''
    return the virtual machine names for all of the images located in the
    butter cloud's local_path in a list:

    ['vm1.boo.com', 'vm2.foo.com']

    CLI Example:
    salt '*' buttervm.local_images <image_path>
    '''
    return os.listdir(local_path)

def full_butter_data(local_path):
    '''
    Return the full virt info, but add butter data!

    CLI Example:
    salt '*' buttervm.full_butter_data <image_path>
    '''
    info = virt.full_info()
    info['local_images'] = local_images(local_path)
    return info

def create(instance, vda, image, pin):
    '''
    Create a virtual machine, this is part of the butter vm system and assumes
    that the files prepared by butter are available via shared storage.
    AKA - don't call this from the command line!

    Arguments:
    instance - string, The path to the instance directory for the given vm on
    shared storage
    vda - The location where the virtual machine image needs to be placed
    image - The image to move into place
    pin - a "pin" data structure defining the myriad of possible vdb-vbz disk
    images to generate.
    '''
    # Generate convenience data
    fqdn = os.path.basename(instance)
    local_path = os.path.dirname(vda)
    overlay = os.path.join(instance, overlay)
    _place_image()
    _gen_pin_drives(local_path, pin)
    _apply_overlay(vda, overlay)
