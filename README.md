# Manyland Texture Importer
A tool I created to help import drawings/pixel art I made into the world of Manyland. Please note that while you can use this tool to import copyrighted drawings into Manyland, it is advisable to avoid doing so, because, well... They're copyrighted drawings!

## Installation
I recommend using [Git Bash](https://gitforwindows.org/) for installing, as it comes prepackaged with pip.

I recommend using [Anaconda](https://anaconda.org/takluyver/mingw-w64) to help with installations. Once you have it installed, do:
```bash
conda activate
```
You should see "(base)" above the commands if you have conda activated.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Pillow, a Python library I use to extract .png data.
```bash
pip install Pillow
```




## Usage

After extracting, go inside folder to where you can see the .py scripts and run:  python imageToDynamic.py editedPhotos/waterWraith.png to test the scripts. If it works, it should create a file in ROOMOutput called "ROOMwaterWraith.png.js" (or overwrite it, if it's already there).

As an example, say I wanted to import a whiteboard drawing, "waterWraith.png":

![Water Wraith Example](editedPhotos/waterWraith.png "Water Wraith from Pikmin 2 poppin' a sick wheelie!")

Note that the imported image must be a .png formatted with transparency, and that the image should have 55 or less colors (Gimp's indexed mode is your friend!)

The image I'm importing is 152x152 pixels. Since a 3x3 cell dynamic is 89x89 pixels, the resulting image will be imported as 4 dynamics.

I would use:
```bash
python imageToDynamic.py editedPhotos/waterWraith.png
```
Which should output something like:
```bash
        Outputting to: editedPhotos/waterWraith , Roomname:  waterWraith.png
        Required cells: 36 to fit a 152 x 152 image.
        Finished writing: editedPhotos/waterWraith
```

This will create ROOMOutput/ROOMwaterWraith.png.js. Open it up an copy the javascript code inside, then open up Manyland (note that the Steam version of Manyland doesn't play nice with javascript, so you'll have to use the browser version.

Create a new changer, paste the javascript code into it, and hit the CTRL+S button to run the changer once. The changer's sprite will change to a preview of whatever you imported from somewhere in the middle of the original image (note that if the original image was transparent, you might not notice any change, that's fine). For the water wraith example, you'd see:
![Whiteboard changer preview](demo/ChangerDemo.png "A bit of black marker stickin' out from the example image.")

Click the green check mark to save the changer. Now, start creating a 9 cell dynamic but DON'T hit the green check mark yet. Instead, click on the newly-created changer on the menu on the right-side of the screen (this would be "photo cha..." in the following screenshot). The dynamic cells should change to whatever's in the image you're trying to import:
![Whiteboard changer preview](demo/ChangerDemo2.png "The water wraith's face.")


By default, the resulting dynamic will be whatever's in the top-left 89x89 square of the imported image. To get the other 3 quadrants of the water wraith, you can add [x,y] to the dynamic's name. For instance, if I wanted to get the top-right of the water wraith, I'd name it "[1,0] example", then click on the changer like before.

Here's how the resulting 4 water wraith dynamics look like in-game. Note that I already added code to the dynamics to positions their cells to fit together nicely.
![The Result](demo/ChangerDemo3.png "Voila!")

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)