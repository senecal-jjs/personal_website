title: Acoustic Wavenumber Spectroscopy
date: 2018-07-13
link: aws

Link to paper: <a target="_blank" href="{{ url_for('static', filename="pdf/IWSHM Manuscript.pdf") }}">Click here</a>

Acoustic Wavenumber Spectroscopy (AWS) identifies damage in a two-dimensional 
scan of a structure on a pixel by pixel basis, by estimating the wavenumber of a 
structure's response to a steady-state, single frequency, ultrasonic excitation.
A laser doppler vibrometer is used to measure a structure's response (known as lamb waves) 
to the ultrasonic excitation. When the lamb waves encounter a defect, (i.e. a crack, corrosion) 
the local wavelength of the lamb waves change and the change in wavelength can be detected
using specialized signal processing techniques.

After processing the raw pattern acoustic wavenumber spectroscopy can produce images like 
the one shown below, which shows a scan of a composite wing section. The bright blue areas are
structural elements below the skin, while the bright red circle is a damaged area. 

<div class="img_row">
    <img class="col-5" src="{{ url_for('static', filename="img/wing.jpg") }}">
</div>

Commercial laser doppler vibrometers cost in the $60,000 to $80,000 range. While at Los Alamos 
National Laboratory I developed a much more compact, and simplified laser doppler vibrometer 
which costs on the order of $10,000. The key to achieving simplicity was leveraging some of the 
characteristics of acoustic wavenumber spectroscopy (AWS). Namely, that AWS works using a single, known, steady-state frequency. Signal to noise requirements can be relaxed as measurements can be filtered for that specific known frequency. 

<div class="img_row">
    <img class="col-5" src="{{ url_for('static', filename="img/ldv.png") }}">
</div>

<div class="col-12 caption">
    The prototype laser doppler vibrometer I developed. The scanning head is small enough to be held 
    in one hand. 
</div>

The raw images produced by the laser doppler vibrometer scans show a wave pattern
produced by the ultrasonic transducer excitation. This wave pattern is then fed 
through signal processing algorithms to assess changes in spatial wavelength.

<div class="img_row">
    <img class="col-8" src="{{ url_for('static', filename="img/dmg.png") }}">
</div>

<div class="col-12 caption">
    Here we see an example scan of a 5mm thick, aluminum plate. 
    The image on the right displays the wave pattern observed in the plate. In the 
    upper right portion of the scan you can observe a more intense, brighter wave 
    pattern corresponding to thinning in the aluminum plate, which emulates corrosion. 
</div>
