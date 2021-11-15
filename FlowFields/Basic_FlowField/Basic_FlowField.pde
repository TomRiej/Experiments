FlowField flowField;
Particle[] particles;
int numParticles = 15000;


void setup() {
    // fullScreen();
    size(600, 600);
    flowField = new FlowField(10);
    flowField.update();

    particles = new Particle[numParticles];
    for (int i = 0; i < numParticles; i++) {
        PVector start = new PVector(random(600), random(600));
        particles[i] = new Particle(start, random(2,5));
    }
    
}


void draw() {
    background(255);
    flowField.update();

    strokeWeight(2);
    for (Particle p : particles) {
        p.follow(flowField);
    }
}