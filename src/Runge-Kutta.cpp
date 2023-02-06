#include <iostream>
#include <cmath>
#include <fstream>
#include <iomanip>
#include "json.hpp"

//Define Ion
typedef struct
{
char name[20];
double mass;
double charge;
} ion_type;
const double massunit = 1.67e-27;
const double chargeunit = 1.6e-19;
const int ion_nums = 2;
ion_type ion_types[ion_nums] = {
    {"oxygen",16.0 * massunit,chargeunit},
    {"proton",1.0 * massunit,chargeunit}
};

// Parameter struct
struct Parameters {
    ion_type ion = ion_types[0];
    double electric_field = 1.0e-4;
    double init_v_perp_eV = 0.01;
    double init_v_para_eV = 0.01;
    double max_v_para_for_resonance_eV = 10000.0;
    double occur_duration = 1.0;
    double occur_period = 1.0;
    double accele_t_max = 1000.0;
    double L_shell = 10.0;
    double init_Inval_lat_deg = 75.0;
    double dx_para_grid = 1e3;
    double dt = 0.001;
    double T = 200.0;
    int write_out_times = 10;
    double enable_lat_decrease = 1.0;
    double B_amplitude = 0.0;

    double mass;
    double electric_acceleration;
    double init_v_perp = sqrt(init_v_perp_eV*(1.60218e-19)*2.0/mass);
    double init_v_para = sqrt(init_v_para_eV*(1.60218e-19)*2.0/mass);
    double max_v_para_for_resonance = sqrt(max_v_para_for_resonance_eV*(1.60218e-19)*2.0/ion.mass);
    double R_e = 6.3e6;
    double init_Inval_lat = init_Inval_lat_deg/180.0*3.141592;
};

// Reads the parameters from a JSON file
void read_params_from_file(const std::string& filename, Parameters& params) {
    std::ifstream ifs(filename);
    if (!ifs) {
    std::cerr << "Could not open " << filename << " for reading." << std::endl;
    exit(1);
    }

    nlohmann::json json_params;
    ifs >> json_params;
    for(int i = 0;i<ion_nums;i++){
        if(json_params["ion_name"].get<std::string>() == ion_types[i].name){
            params.ion = ion_types[i];
        }
    }
    params.electric_field = 1e-3*json_params["electric_field_mV/m"].get<double>();
    params.init_v_perp_eV = json_params["init_v_perp_eV"].get<double>();
    params.init_v_para_eV = json_params["init_v_para_eV"].get<double>();
    params.max_v_para_for_resonance_eV = json_params["max_v_para_for_resonance_eV"].get<double>();
    params.occur_duration = json_params["occur_duration"].get<double>();
    params.occur_period = json_params["occur_period"].get<double>();
    params.accele_t_max = json_params["accele_t_max"].get<double>();
    params.L_shell = json_params["L_shell"].get<double>();
    params.init_Inval_lat_deg = json_params["init_Inval_lat_deg"].get<double>();
    params.dx_para_grid = json_params["dx_para_grid"].get<double>();
    params.dt = json_params["dt"].get<double>();
    params.T = json_params["T"].get<double>();
    params.write_out_times = json_params["write_out_times"].get<double>();
    params.enable_lat_decrease = json_params["enable_lat_decrease"].get<int>();
    params.B_amplitude = json_params["B_amplitude"].get<double>();
    
    //Input value adjustment
    params.mass = params.ion.mass;
    params.electric_acceleration = params.electric_field*params.ion.charge/params.mass;
    params.init_v_perp = sqrt(params.init_v_perp_eV*(1.60218e-19)*2.0/params.mass);
    params.init_v_para = sqrt(params.init_v_para_eV*(1.60218e-19)*2.0/params.mass);
    params.max_v_para_for_resonance = sqrt(params.max_v_para_for_resonance_eV*(1.60218e-19)*2.0/params.ion.mass);
    params.R_e = 6.3e6;
    params.init_Inval_lat = params.init_Inval_lat_deg/180.0*3.141592;

}



double apply_field(double field, double v_para,double t, const Parameters& params){
    if((v_para>params.max_v_para_for_resonance||fmod(t,params.occur_period)>params.occur_duration)||params.accele_t_max<t){
        return 0.0;
    }else{
        return field;
    }
}

double apply_electric_acceleration(double v_para,double t, const Parameters& params){
    return apply_field(params.electric_acceleration, v_para, t, params);
}

double apply_magnetic_field(double v_para,double t, const Parameters& params){
    return params.B_amplitude;//apply_field(B_amplitude, v_para, t);
}

double grad_field(double inval_lat, const Parameters& params){
    return 3.0*sin(inval_lat)*(5.0*sin(inval_lat)*sin(inval_lat)+3.0)
/(pow((1.0+3.0*sin(inval_lat)*sin(inval_lat)),1.5)*cos(inval_lat)*cos(inval_lat))
*(1.0/(params.R_e*params.L_shell));
}

double dlambda(double inval_lat, const Parameters& params){
    return 1.0/(params.R_e*params.L_shell*cos(inval_lat)*sqrt(1.0+3.0*sin(inval_lat)*sin(inval_lat)));
}

//Calculation
double dv_para(double v_perp, double v_para, double t, double inval_lat, const Parameters& params) {
    double B_wave = apply_magnetic_field(v_para, t, params);
    return grad_field(inval_lat,params) * 0.5 * pow(v_perp, 2.0) + params.ion.charge * B_wave/params.ion.mass * v_perp;
}

double dv_perp(double v_perp, double v_para, double t, double inival_lat, const Parameters& params) {
    double dv_perp_val = apply_electric_acceleration(v_para, t, params) - v_para / v_perp * dv_para(v_perp, v_para, t, inival_lat, params);
    return dv_perp_val;
}

int main() {
    Parameters params_get;
    read_params_from_file("src/params.json", params_get);
    const Parameters params = params_get;

    double v_perp = params.init_v_perp;
    double v_para = params.init_v_para;
    double v_para_prev_x = params.init_v_para;
    double t = 0.0;
    double inval_lat = params.init_Inval_lat;
    int write_out_count = 0;

    //Values for x direction plot
    double x_para = 0.0;
    double x_para_grid = params.dx_para_grid;
    double dx_para = 0.0;
    double t_per_para_grid = 0.0;
    double first_t_per_para_grid = 0.0;
    double first_v_para = 0.0;
    int firstcount_for_grid = 0;
    

    std::ofstream ofs_t("./data/result_t.csv");
    ofs_t << "time,v_perp,v_para,pitch_angle,v_perp_eV,v_para_eV,inval_lat" << std::endl;
    std::ofstream ofs_x("./data/result_x.csv");
    ofs_x << "x,time,relative_density,v_perp,v_para,pitch_angle,v_perp_eV,v_para_eV,energy,energy_density,inval_lat" << std::endl;

    double T = params.T;
    double dt = params.dt;    
    while (t < T && v_perp > 0.0) { // v_perp<0で止める
        //RK4
        double k1_perp = dv_perp(v_perp, v_para, t, inval_lat, params);
        double k1_para = dv_para(v_perp, v_para, t,inval_lat, params);

        double k2_perp = dv_perp(v_perp + 0.5 * dt * k1_perp, v_para + 0.5 * dt * k1_para, t+0.5*dt, inval_lat, params);
        double k2_para = dv_para(v_perp + 0.5 * dt * k1_perp, v_para + 0.5 * dt * k1_para, t+0.5*dt,inval_lat, params);

        double k3_perp = dv_perp(v_perp + 0.5 * dt * k2_perp, v_para + 0.5 * dt * k2_para, t+0.5*dt, inval_lat, params);
        double k3_para = dv_para(v_perp + 0.5 * dt * k2_perp, v_para + 0.5 * dt * k2_para, t+0.5*dt, inval_lat, params);

        double k4_perp = dv_perp(v_perp + dt * k3_perp, v_para + dt * k3_para, t+dt, inval_lat, params);
        double k4_para = dv_para(v_perp + dt * k3_perp, v_para + dt * k3_para, t+dt, inval_lat, params);
        v_perp += dt / 6.0 * (k1_perp + 2.0 * k2_perp + 2.0 * k3_perp + k4_perp);
        v_para += dt / 6.0 * (k1_para + 2.0 * k2_para + 2.0 * k3_para + k4_para);
        t += dt;
        dx_para= v_para*dt;
        //End RK4

        //RK4 for lambda
        double k1_lambda = dlambda(inval_lat,params);
        double k2_lambda = dlambda(inval_lat - 0.5 * dx_para * k1_lambda,params);
        double k3_lambda = dlambda(inval_lat - 0.5 * dx_para * k2_lambda,params);
        double k4_lambda = dlambda(inval_lat - dx_para * k3_lambda,params);
        inval_lat -= dx_para / 6.0 * (k1_lambda + 2.0 * k2_lambda + 2.0 * k3_lambda + k4_lambda);

        //WriteOut section(Time plot)
        double pitch_angle = atan2(v_perp,v_para)*180/(3.1415926535);
        double v_perp_eV = 0.5*params.mass*v_perp*v_perp/(1.60218e-19);
        double v_para_eV = 0.5*params.mass*v_para*v_para/(1.60218e-19);

        write_out_count += 1;
        if(write_out_count>params.write_out_times){
            ofs_t << t << "," << v_perp << "," << v_para << "," << pitch_angle<< "," << v_perp_eV << "," << v_para_eV << "," << inval_lat/3.14159265*180 << std::endl;
            write_out_count = 0;
        }

        //WriteOut section(x plot)
        x_para += fabs(dx_para);
        t_per_para_grid += dt;
        if(x_para>x_para_grid){
            if(firstcount_for_grid == 0){
                first_t_per_para_grid = t_per_para_grid;
                first_v_para = fabs(v_para);
                firstcount_for_grid += 1;
            }

            x_para_grid += params.dx_para_grid;
            int proceed_count = 1;
            while (x_para>x_para_grid)
            {
                x_para_grid += params.dx_para_grid;
                proceed_count++;
            }
            double dv_paradx = abs(v_para-v_para_prev_x);
            
            ofs_x << x_para_grid/1e3 << "," << t << "," << 1.0 << "," << v_perp << "," << v_para << "," << pitch_angle<< "," << v_perp_eV << "," << v_para_eV << "," << v_para_eV+v_perp_eV << "," << (v_para_eV+v_perp_eV) << "," << inval_lat/3.141592*180.0 << std::endl;
            // flux = constant, so 1/v_para = relative_density, I think

            // prev ver relative_density (It's wrong)
            // t_per_para_grid/first_t_per_para_grid

            v_para_prev_x = v_para;
            t_per_para_grid = 0.0;
        }

    }

    if(v_perp<0.0){
        std::cout<<"Simulation is stopped because v_perp<0"<<"\n";
    }

    ofs_t.close();
    ofs_x.close();


    //Execute Python
    std::string command = "python3 ./src/plot.py ";
    std::system(command.c_str());

    return 0;

}