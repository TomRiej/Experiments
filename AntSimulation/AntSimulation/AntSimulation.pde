int numAnts = 2000;
Ant[] ants = new Ant[numAnts];


void setup() {
  size(800, 800);
  colorMode(HSB, 360, 100, 100);
  for (int i = 0; i<numAnts; i++) {
    ants[i] = new Ant(400, 400);
  }
}

void draw() {
  background(0);
  stroke(255);
  for (Ant a : ants) {
    a.update();
    a.display();
  }
}
