#include <iostream>
#include <cmath>
#include <fstream>
#include <iomanip>

//Define Ion
typedef struct  
{
  char name[20];  
  double mass;
} ion_type;
const double massunit = 1.6e-27;
const ion_type oxygen{"oxygen",16.0*massunit};
const ion_type proton{"proton",1.0*massunit};

////Parameter
//Graphs_file_name_param
const ion_type ion = oxygen;
const double electric_field = 1.0e-3;
const double init_v_perp_eV = 0.1;
const double init_v_para_eV = 0.1;
const double max_v_para_for_resonance_eV = 100.0;
const double occur_duration = 1.0;
const double occur_period = 1.0;//occur_period秒の間にoccur_duration秒共鳴加速が発生
//Graphs_file_No_name_param
const double L_shell = 10.0;
const double Inval_lat_deg = 70.0;
const double dx_para_grid = 1e3;//(m)
const double dt = 0.001;//(s)
const double T = 300.0;//(s)
const int write_out_times = 10; // How many calculations do you write once?
////


//Input value adjustment
const double mass = ion.mass;
const double electric_acceleration = electric_field*1.6e-19/mass;
const double init_v_perp = sqrt(init_v_perp_eV*(1.60218e-19)*2.0/mass);
const double init_v_para = sqrt(init_v_para_eV*(1.60218e-19)*2.0/mass);
const double max_v_para_for_resonance = sqrt(max_v_para_for_resonance_eV*(1.60218e-19)*2.0/mass);
const double R_e = 6.3e6;
const double Inval_lat = Inval_lat_deg/180.0*3.141592;
const double grad_field = 3.0*sin(Inval_lat)*(5.0*sin(Inval_lat)*sin(Inval_lat)+3.0)
/(pow((1.0+3.0*sin(Inval_lat)*sin(Inval_lat)),1.5)*cos(Inval_lat)*cos(Inval_lat))
*(1.0/(R_e*L_shell));

//Calculation
double dv_para(double v_perp, double v_para) {
    return grad_field * 0.5 * pow(v_perp, 2.0);
}

double dv_perp(double v_perp, double v_para, double t) {
    double dv_perp_val = electric_acceleration - v_para / v_perp * dv_para(v_perp, v_para);
    if(v_para>max_v_para_for_resonance||fmod(t,occur_period)>occur_duration){
        dv_perp_val = - v_para / v_perp * dv_para(v_perp, v_para);
    }
    return dv_perp_val;
}

int main() {
    double v_perp = init_v_perp;
    double v_para = init_v_para;
    double t = 0.0;
    int write_out_count = 0;

    //Values for x direction plot
    double x_para = 0.0;
    double x_para_grid = dx_para_grid;
    double t_per_para_grid = 0.0;
    double first_t_per_para_grid = 0.0;
    int firstcount_for_grid = 0;
    

    std::ofstream ofs_t("./data/result_t.csv");
    ofs_t << "time,v_perp,v_para,pitch_angle,v_perp_eV,v_para_eV" << std::endl;
    std::ofstream ofs_x("./data/result_x.csv");
    ofs_x << "x,relative_density,v_perp,v_para,pitch_angle,v_perp_eV,v_para_eV" << std::endl;

    //RK4
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
        //End RK4

        //WriteOut section(Time plot)
        double pitch_angle = atan2(v_perp,v_para)*180/(3.1415926535);
        double v_perp_eV = 0.5*mass*v_perp*v_perp/(1.60218e-19);
        double v_para_eV = 0.5*mass*v_para*v_para/(1.60218e-19);

        write_out_count += 1;
        if(write_out_count>write_out_times){
            ofs_t << t << "," << v_perp << "," << v_para << "," << pitch_angle<< "," << v_perp_eV << "," << v_para_eV << std::endl;
            write_out_count = 0;
        }

        //WriteOut section(x plot)
        x_para += v_para*dt;
        t_per_para_grid += dt;
        if(x_para>x_para_grid){
            if(firstcount_for_grid == 0){
                first_t_per_para_grid = t_per_para_grid; //For normalize t_per_para_grid
                firstcount_for_grid += 1;
            }

            ofs_x << x_para_grid/1e3 << "," << t_per_para_grid/first_t_per_para_grid << "," << v_perp << "," << v_para << "," << pitch_angle<< "," << v_perp_eV << "," << v_para_eV << std::endl;
            x_para_grid += dx_para_grid;

            while (x_para>x_para_grid)
            {
                x_para_grid += dx_para_grid;
            }
            t_per_para_grid = 0.0;
        }

    }
    ofs_t.close();
    ofs_x.close();

    //Send parameter to Python
    int outdigit = 2;
    std::stringstream ss1, ss2, ss3, ss4, ss5, ss6;
    ss1 << std::fixed << std::setprecision(outdigit) << init_v_para_eV;
    std::string init_v_para_ev_str =ss1.str(); 
    ss2 << std::fixed << std::setprecision(outdigit) << init_v_perp_eV;
    std::string init_v_perp_ev_str =ss2.str(); 
    ss3 << std::fixed << std::setprecision(outdigit) << max_v_para_for_resonance_eV;
    std::string max_v_para_for_resonance_eV_str =ss3.str(); 
    ss4 << std::fixed << std::setprecision(outdigit) << electric_field*1e3;
    std::string electric_field_str =ss4.str(); 
    ss5 << std::fixed << std::setprecision(outdigit) << occur_duration;
    std::string occur_duration_str =ss5.str(); 
    ss6 << std::fixed << std::setprecision(outdigit) << occur_period;
    std::string occur_period_str =ss6.str(); 

    std::ofstream ofs("./data/params.txt");
    ofs << ion.name << std::endl;
    ofs << init_v_para_ev_str << std::endl;
    ofs << init_v_perp_ev_str << std::endl;
    ofs << max_v_para_for_resonance_eV_str << std::endl;
    ofs << electric_field_str << std::endl;
    ofs << occur_duration_str << std::endl;
    ofs << occur_period_str << std::endl;
    ofs.close();


    //Execute Python
    std::string command = "/bin/python3 ./src/plot_for_x.py ";
    std::system(command.c_str());

    return 0;

}