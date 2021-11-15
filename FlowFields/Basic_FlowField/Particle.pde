public class Particle{
    PVector pos, vel, acc;
    float maxSpd;
    int x, y;

    Particle(PVector start, float maxSpeed){
        maxSpd = maxSpeed;
        pos = start;
        vel = new PVector(0, 0);
    }

    void update() {
        pos.add(vel);
        vel.limit(maxSpd);
    }

    void edges() {
        if (pos.x > 600) pos.x = 0;
        else if (pos.x < 0) pos.x = 600;
        if (pos.y > 600) pos.y = 0;
        else if (pos.y < 0) pos.y = 600;
    }

    void follow(FlowField flowField) {
        x = floor(pos.x / flowField.res);
        y = floor(pos.y / flowField.res);
        vel.add(flowField.vectors[x + y * flowField.cols]);
        update();
        edges();
        stroke(0);
        point(pos.x, pos.y);
    }
}