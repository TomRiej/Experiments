class Ant {
  PVector coords;
  PVector vel;
  float theta = PI/16;

  Ant(int x, int y) {
    coords = new PVector(x, y);
    vel = PVector.random2D();
  }
  void update(){
    // decide whether to wander or follow 
    wander();
  }

  void wander() {
    // rotate the ant
    vel.rotate(random(-theta, theta));

    // move the ant
    coords.add(vel);
    if (coords.x < 0 || coords.x > 800) {
      coords.sub(vel);
      vel.x *= -1;
    } else if (coords.y < 0 || coords.y > 800) {
      coords.sub(vel);
      vel.y *= -1;
    }
  }

  void display() {
    ellipse(coords.x, coords.y, 3, 3);
  }
}
