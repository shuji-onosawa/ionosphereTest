# plot_pitch_angle.py

ピッチ角分布の時間変化**もどき**を計算することができます。

モデルが雑すぎてぶっちゃけ、「おもちゃ」だと思いますw。

ここで、「上」は高度が高い、「下」は高度が低いことを意味します。

説明
以下のような状況を想定したプロットです。非常に単純なモデルから作成するプロットなので、たくさんの仮定があります。
- とある、磁力線方向に高さを持った領域（以下、「電場加速領域」）で、acceleration_time秒だけ、加速のために必要な電場が発生します。その領域は、今いる地点、すなわち観測地点から「distance_accele_area_up」下に進んだ場所が電場加速領域の「上限」で、「distance_accele_area_low」下に進んだ場所が電場加速領域の「下限」です。

- その加速領域では、常に粒子が供給されます。そして、電場加速領域内のすべての場所で「常に同じだけの量の粒子が加速」されています。場所によって、より多くの粒子が加速される、といったことはありません。

- 電場加速領域で加速された粒子はミラーフォースにより、上に向かって行きます。電場加速領域では常に同じだけの量の粒子が加速され続けていますから、時間差を持って、様々な粒子が上に向かって飛んでいきます。そして、それを観測地点で見た時、どれぐらいのピッチ角の粒子がどれぐらいの密度、エネルギー密度で存在しますか、というグラフを表示します。

- 当然、電場加速領域以外の粒子の影響は加味されません。これは、以下のような仮定から導かれます。
    - 電場で加速された粒子のみが、強いエネルギーを持ち、衛星でピッチ角分布を観測される粒子になる。
    - 電場加速領域以外で加速された粒子はいない。

- 対流などは当然考えていません。電場加速領域で加速された粒子が、そのままミラーフォース以外の力は何も受けずに磁力線に沿って観測地点に飛んできます。

- **粒子が電場加速を抜けたことによって加速が停止する効果は含まれていません** すべての粒子は電場加速領域を抜ける前に、共鳴条件が破れる、という仮定を置いています。これは、共鳴条件が破れる前に粒子が磁力線に沿って進む距離が極めて短いだろう、という仮定に基づいています、が...　ぶっちゃけモデルの都合です。この仮定がどれほど正しいかは、以下の情報を参考にしてください。
    - 酸素イオンが平行方向垂直方向に0.1eVの速度を持って、磁気緯度70度、L = 10程度から加速がスタートしたとします。電場は常にコンスタントに1.0mV/mで垂直に酸素イオンを加速していきます。このとき平行方向にある速度になり、共鳴条件が破れたとします。ある速度が1eV、10eV、100eVのとき、このモデルでは...
        - 1eV
            - 加速が終わるまでに進んだ距離 17km
            - かかった時間 10s
            - 垂直方向 300eV前後まで加速
        - 10eV
            - 加速が終わるまでに進んだ距離 57km
            - かかった時間 15s
            - 垂直方向 750eV前後まで加速
        - 100eV
            - 加速が終わるまでに進んだ距離 240km
            - かかった時間 24s
            - 垂直方向 1650eV前後まで加速

    - 100eVになるまで加速しているとは考えづらい..　とか甘いこと考えておくと、200km ぐらいのスケール、あるいは電場加速領域からの距離があれば、ある程度正当化されるかもしれません。
    - この効果ちゃんと入れようと思ったら、初期位置の異なる様々な粒子を計算しなくちゃいけなくて面倒くさいので、面倒くさいんだったら、これで我慢しましょう（）。

- 当然ですが、もともとものシミュレーション内で観測高度に到達していないと、計算できません。(シミュレーション内で進んだ距離が電場加速領域と観測場所の距離より短いとダメです)

以上です。最初に行った通り、「おもちゃ」ですが、まあ遊べるとは思います。

--- 

## From Chat GPT Summary

The above script is used to process and visualize data from a simulation of charged particles in a magnetic field. The script first defines a function initialize_parameters() which sets some default values for parameters used in the script, such as the upper and lower distance limits for the acceleration area, the time step (dt), and the total acceleration and observation times.

The script then reads in data from a file './data/result_x.csv' using the Pandas library and filters the data based on the distance limits specified in the parameters. It also reads in other parameters from a file './data/params.txt'

The script then initializes lists to store relative density and energy density sums, and then iterates over pitch angles and time steps, filtering the data and summing the relative density and energy density for each iteration.

Finally, the script creates a plot of the energy density sums using Matplotlib and a colormesh plot of the relative density sums. The script also includes logic to handle cases where the user wants a logarithmic plot.

---

## From ChatGPT detail

The script starts by importing the necessary libraries (numpy, pandas, and matplotlib) and defining a function called initialize_parameters(). This function creates a dictionary called params and assigns default values to various parameters that will be used later in the script. These include a boolean value indicating whether or not to use a log scale, upper and lower distances for an acceleration area (in kilometers), time step (dt) for calculations, and the time for acceleration and observation.

The script then calls the initialize_parameters() function to create the params dictionary and assigns it to the variable params. It then checks that the upper distance is smaller than the lower distance, and if not, prints an error message and exits the script.

The script then reads parameters from a file called "params.txt" that is located in the "data" directory. The parameters are read as a list of strings and are then assigned to various variables, such as ion_name, init_v_para_eV, init_v_perp_eV, max_v_para_for_resonance_eV, electric_field, occur_duration, occur_period, and accele_t_max.

The script then reads in a csv file called "result_x.csv" located in the "data" directory using the pandas library. It filters the data by the distance using the upper_distance_acceleration_area and lower_distance_acceleration_area parameters from the params dictionary.

The script then defines a list of pitch angles and calculates the minimum and maximum times from the time data in the filtered dataframe. It also calculates the number of time steps using the observe_time and dt parameters from the params dictionary.

The script then initializes two 2D lists called relative_density_sums and energy_density_sums that will be used to store the sums of relative density and energy density for each pitch angle and time step.

The script then loops over the pitch angles and time steps, filtering the data based on the current pitch angle range and time range, and summing the relative density and energy density for each iteration.

After the loops have finished, the script creates a list of times for plotting using the t_min and dt parameters from the params dictionary.

The script then creates a figure with subplots using matplotlib and plots the energy density sums on the first subplot. The x-axis is labeled as "t", the y-axis is labeled as "pitch_angle" and the colorbar is labeled as "erg_density". It also plots the relative density sums on the second subplot. The x-axis is labeled as "t", the y-axis is labeled as "pitch_angle" and the colorbar is labeled as "rel_density".

It also check if want_log is true, it will create another two subplots for log scale. The third subplot will show the energy density sums on the log scale and the fourth subplot will show the relative density sums on the log scale.

In summary, this script reads in data from two files, filters the data based on specified distances and pitch angles, and then plots the relative density and energy density sums for each pitch angle and time step.