from statistics import mean
import ShizukuRecFileExtractor

if __name__=="__main__":
    fmt='.2f'
    total_energy = 0.0
    total_capacity = 0.0
    vbus = []
    ibus = []
    try:
        with ShizukuRecFileExtractor.reader('/path/to/file.ShizukuRec') as fd:
                
            for record in ShizukuRecFileExtractor.get_record(fd):
                total_energy += record._energy
                total_capacity += record._capacity
                vbus.append(record._vbus)
                ibus.append(record._ibus)
                print(f"{record}")
            else:
                duration_s = record._time_ms // 1000 * int(record._dt * 3600)
                h, m, s = [duration_s // 3600, duration_s % 3600 // 60, duration_s % 3600 % 60]

                print(f"Duration: {h} h {m} min {s} s")
                
                print(f"Min/Max/Avg current: {min(ibus):{fmt}} / {max(ibus):{fmt}} / {mean(ibus):{fmt}} [A]" )
                print(f"Min/Max/Avg voltage: {min(vbus):{fmt}} / {max(vbus):{fmt}} / {mean(vbus):{fmt}} [V]" )
                
                print(f"Uses average: {total_energy / (duration_s / 3600):.2f} [W]" )

                print(f"Total energy: {total_energy:{fmt}} [Wh]")
                print(f"Total capacity: {total_capacity:{fmt}} [Ah]")
    
    except Exception as e:
        print(e)