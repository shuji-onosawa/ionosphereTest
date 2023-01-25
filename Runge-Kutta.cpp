#include <iostream>
#include <cmath>
#include <fstream>

const double electric_acceleration = 1e5/16.0;
const double grad_field = 2.5e-9;
const double dt = 0.001;
const double T = 1200.0;

double dv_para(double v_perp, double v_para) {
    return grad_field * pow(v_perp, 2.0);
}

double dv_perp(double v_perp, double v_para, double t) {
    double dv_perp_val = electric_acceleration - v_para / v_perp * dv_para(v_perp, v_para);
    if(v_para>3.5e5||fmod(t,5.0)>1.0){
        dv_perp_val = - v_para / v_perp * dv_para(v_perp, v_para);
    }
    return dv_perp_val;
}

int main() {
    double v_perp = 1.1e3;
    double v_para = 1.1e3;
    double t = 0.0;

    std::ofstream ofs("result.csv");
    ofs << "time,v_perp,v_para,pitch_angle" << std::endl;

    while (t < T) {
        double k1_perp = dv_perp(v_perp, v_para, t);
        double k1_para = dv_para(v_perp, v_para);

        double k2_perp = dv_perp(v_perp + 0.5 * dt * k1_perp, v_para + 0.5 * dt * k1_para, t+0.5*dt);
        double k2_para = dv_para(v_perp + 0.5 * dt * k1_perp, v_para + 0.5 * dt * k1_para);

        double k3_perp = dv_perp(v_perp + 0.5 * dt * k2_perp, v_para + 0.5 * dt * k2_para, t+0.5*dt);
        double k3_para = dv_para(v_perp + 0.5 * dt * k2_perp, v_para + 0.5 * dt * k2_para);

        double k4_perp = dv_perp(v_perp + dt * k3_perp, v_para + dt * k3_para, t+dt);
        double k4_para = dv_para(v_perp + dt * k3_perp, v_para + dt * k3_para);
        v_perp += dt / 6.0 * (k1_perp + 2.0 * k2_perp + 2.0 * k3_perp + k4_perp);
        v_para += dt / 6.0 * (k1_para + 2.0 * k2_para + 2.0 * k3_para + k4_para);
        t += dt;

        double pitch_angle = atan2(v_perp,v_para)*180/(3.1415926535);

        ofs << t << "," << v_perp << "," << v_para << "," << pitch_angle << std::endl;
    }

    ofs.close();

    std::system("/bin/python3 /home/skipjack/Documents/ionosphereTest/plot.py");

    return 0;

}