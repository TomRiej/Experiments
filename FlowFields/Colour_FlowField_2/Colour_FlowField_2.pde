FlowField flowField;
Particle[] particles;
int numParticles = 25000;
int screenSize = 800;


void setup() {
    // fullScreen();
    size(800, 800);
    colorMode(HSB, 360, 100, 100, 255); 
    flowField = new FlowField(10);
    flowField.update();

    particles = new Particle[numParticles];
    for (int i = 0; i < numParticles; i++) {
        PVector start = new PVector(random(screenSize), random(screenSize));
        particles[i] = new Particle(start, random(2,5), screenSize);
    }
    
}


void draw() {
    background(0);
    flowField.update();

    strokeWeight(1);
    for (Particle p : particles) {
        p.follow(flowField);
    }
}
