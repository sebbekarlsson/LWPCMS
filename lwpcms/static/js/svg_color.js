function color_svgs() {
    var svgs = document.querySelectorAll('object');
    for (i = 0; i < svgs.length; ++i) {

        svgs[i].addEventListener('load', function() {

            var doc = this.getSVGDocument();
            var svg = doc.querySelector("svg");
            svg.setAttribute("fill", this.getAttribute('fill'));

        });

    }
}
