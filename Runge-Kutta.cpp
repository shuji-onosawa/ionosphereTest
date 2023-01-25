#include <iostream>
#include <cmath>
#include <fstream>


const double mass = 1.6e-27*16.0;
const double electric_field = 1.0e-3;
const double electric_acceleration = electric_field*1.6e-19/mass;
const double init_v_perp_eV = 0.1;
const double init_v_para_eV = 0.1;
const double init_v_perp = sqrt(init_v_perp_eV*(1.60218e-19)*2.0/mass);
const double init_v_para = sqrt(init_v_para_eV*(1.60218e-19)*2.0/mass);
const double max_v_para_for_resonance_eV = 1.0;
const double max_v_para_for_resonance = sqrt(max_v_para_for_resonance_eV*(1.60218e-19)*2.0/mass);
const double R_e = 6.3e6;
const double L_shell = 10.0;
const double Inval_lat = 70.0 /180.0*3.141592;
const double grad_field = 3.0*sin(Inval_lat)*(5.0*sin(Inval_lat)*sin(Inval_lat)+3.0)
/(pow((1.0+3.0*sin(Inval_lat)*sin(Inval_lat)),1.5)*cos(Inval_lat)*cos(Inval_lat))
*(1.0/(R_e*L_shell));
const double dt = 0.001;
const double T = 300.0;
const int write_out_times = 10;

double dv_para(double v_perp, double v_para) {
    return grad_field * 0.5 * pow(v_perp, 2.0);
}

double dv_perp(double v_perp, double v_para, double t) {
    double dv_perp_val = electric_acceleration - v_para / v_perp * dv_para(v_perp, v_para);
    if(v_para>max_v_para_for_resonance){
        dv_perp_val = - v_para / v_perp * dv_para(v_perp, v_para);
    }
    return dv_perp_val;
}

int main() {
    double v_perp = init_v_perp;
    double v_para = init_v_para;
    double t = 0.0;
    int write_out_count = 0;

    std::ofstream ofs("result.csv");
    ofs << "time,v_perp,v_para,pitch_angle,v_perp_eV,v_para_eV" << std::endl;

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
        double v_perp_eV = 0.5*mass*v_perp*v_perp/(1.60218e-19);
        double v_para_eV = 0.5*mass*v_para*v_para/(1.60218e-19);
        
        write_out_count += 1;
        if(write_out_count>write_out_times){
            ofs << t << "," << v_perp << "," << v_para << "," << pitch_angle<< "," << v_perp_eV << "," << v_para_eV << std::endl;
            write_out_count = 0;
        }
    }

    ofs.close();

    std::system("/bin/python3 /home/skipjack/Documents/ionosphereTest/plot.py");

    return 0;

}