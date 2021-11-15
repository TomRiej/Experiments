class Particle {
    PVector pos;
    PVector vel;
    float size = random(5, 30);
    color colour;

    Particle(int hue) {
        pos = new PVector(mouseX+random(-2, 2), mouseY+random(-2, 2));
        vel = new PVector(random(-2,2), random(-2,2));
        colour = color(hue, 100, 100);
    }

    void update() {
        pos.add(vel);
        size -= 0.2;
    }

    void draw() {
        noStroke();
        fill(colour);
        ellipse(pos.x, pos.y, size, size);
        
    }

    color getColour() {
        return colour;
    }

    float getX() {
        return pos.x;
    }

    float getY() {
        return pos.y;
    }

    boolean finished() {
        return (size < 8.0);
    }

}