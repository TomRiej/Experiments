public class Particle{
    PVector pos, vel, acc;
    float maxSpd;
    int x, y, screenSize;

    Particle(PVector start, float maxSpeed, int size){
        maxSpd = maxSpeed;
        pos = start;
        screenSize = size;
        vel = new PVector(0, 0);
    }

    void update() {
        pos.add(vel);
        vel.limit(maxSpd);
    }

    void edges() {
        if (pos.x > screenSize) pos.x = 0;
        else if (pos.x < 0) pos.x = screenSize;
        if (pos.y > screenSize) pos.y = 0;
        else if (pos.y < 0) pos.y = screenSize;
    }

    void follow(FlowField flowField) {
        x = floor(pos.x / flowField.res);
        y = floor(pos.y / flowField.res);
        vel.add(flowField.vectors[x + y * flowField.cols]);
        update();
        edges();
        stroke(((vel.heading()+PI)/TWO_PI)*360, 100, 100, 255);
        point(pos.x, pos.y);
    }
}