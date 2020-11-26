using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarMovement : MonoBehaviour
{
    public Transform tf;

    public float mass = 1000f;         // kg
    public float velocity = 0.0f;      // Current Travelling Velocity
    public float acc = 0.0f;           // Current Acceleration
    public float displacement;

    public float engineForce = 1000f;  //1000N engine force
    public float coefDrag;             // 0-1
    public float frontalArea = 2.2f;
    public float airDensity = 1.29f;
    public float coefRollingRes;

    private float forwardF;

    private void Start()
    {
        coefDrag = 0.5f; 
        coefRollingRes = coefDrag * 30;
    }

    void Update()
    {
        if (Input.GetKey(KeyCode.W))
        {
            forwardF = engineForce;
        }
        else
        {
            forwardF = 0f;
        }
        
        float dragF = -coefDrag * frontalArea * airDensity * velocity * velocity / 2;
        float rollingResF = -coefRollingRes * velocity;

        float resultantF = forwardF + dragF + rollingResF;

        acc = resultantF / mass;
        velocity += (Time.deltaTime * acc);
        displacement += (Time.deltaTime * velocity);
        tf.Translate(0,0,(displacement - tf.position.z));

       
        
    }

}