ArrayList<Particle> particles = new ArrayList<Particle>();
boolean mouseOnScreen = false;
int hue = 0;
Particle p, p2;
int maxConnections = 5;



void setup() {
    size(1200,800);
    colorMode(HSB, 360, 100, 100);
}

void draw() {
    background(0);
    for (int i = particles.size()-1; i >= 0; i--) {
        p = particles.get(i);
        p.update();
        p.draw();
        if (random(1) < 1) {
            int connects = 0;
            int j = particles.size()-1;
            while (connects < maxConnections && j >= 0) {
                p2 = particles.get(j);
                if (sq(p2.getX() - p.getX()) + sq(p2.getY() - p.getY()) < 5000) {
                    stroke(p.getColour());
                    strokeWeight(0.4);
                    line(p.getX(), p.getY(), p2.getX(), p2.getY());
                    connects++;
                } 
                j--;
            }
        }
        if (p.finished()) {
            particles.remove(i);
        }
    }

    // change colour
    if (hue < 360){
            hue++;
        } else {
            hue = 0;
        }

    // println(particles.size());
}

void mouseMoved() {
    if (mouseOnScreen) {
        particles.add(new Particle(hue));
    }
}

void mouseEntered() {
    mouseOnScreen = true;
}

void mouseExited() {
    mouseOnScreen = false;
}