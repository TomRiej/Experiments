/* autogenerated by Processing revision 1277 on 2021-11-14 */
import processing.core.*;
import processing.data.*;
import processing.event.*;
import processing.opengl.*;

import java.util.HashMap;
import java.util.ArrayList;
import java.io.File;
import java.io.BufferedReader;
import java.io.PrintWriter;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.IOException;

public class Colour_FlowField_1 extends PApplet {

FlowField flowField;
Particle[] particles;
int numParticles = 15000;


 public void setup() {
    /* size commented out by preprocessor */;
    colorMode(HSB, 360, 100, 100, 255);
    flowField = new FlowField(10);
    flowField.update();

    particles = new Particle[numParticles];
    for (int i = 0; i < numParticles; i++) {
        PVector start = new PVector(random(600), random(600));
        particles[i] = new Particle(start, random(2,5));
    }
    
}


 public void draw() {
    background(0);
    flowField.update();

    strokeWeight(2);
    for (Particle p : particles) {
        p.follow(flowField);
    }
}
public class FlowField {
    PVector[] vectors;
    int rows, cols, res;
    float noiseScale = 0.2f;
    float zOff = 0.0f;
    int hue;
    int[] hues;

    FlowField(int r) {
        res = r;
        cols = (600 / res) + 1;
        rows = (600 / res) + 1;
        vectors = new PVector[rows * cols];
        hues = new int[rows * cols];
    }

     public void update() {
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                float n = noise(j*noiseScale, i*noiseScale, zOff)*2;
                vectors[j + i * cols] = PVector.fromAngle(n*TWO_PI);
                hues[j + i * cols] = floor(n*300);
            }
        }
        zOff += 0.005f;
    }
}
public class Particle{
    PVector pos, vel, acc;
    float maxSpd;
    int x, y;

    Particle(PVector start, float maxSpeed){
        maxSpd = maxSpeed;
        pos = start;
        vel = new PVector(0, 0);
    }

     public void update() {
        pos.add(vel);
        vel.limit(maxSpd);
    }

     public void edges() {
        if (pos.x > 600) pos.x = 0;
        else if (pos.x < 0) pos.x = 600;
        if (pos.y > 600) pos.y = 0;
        else if (pos.y < 0) pos.y = 600;
    }

     public void follow(FlowField flowField) {
        x = floor(pos.x / flowField.res);
        y = floor(pos.y / flowField.res);
        vel.add(flowField.vectors[x + y * flowField.cols]);
        update();
        edges();
        stroke(flowField.hues[x + y * flowField.cols], 100, 100, 100);
        point(pos.x, pos.y);
    }
}


  public void settings() { size(600, 600); }

  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "Colour_FlowField_1" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
