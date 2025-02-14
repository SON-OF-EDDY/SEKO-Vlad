from data.database import clients_conf
import fun

def main():
    site_name = input("Введите название сайта или all: ")
    # site_name = "all"
    site_exceptions = ['ekodar', 'ovkcompany-shop']
    if site_name == 'all':
        for site_name in clients_conf.keys():
            if site_name not in site_exceptions:
                print('Обработка сайта: ', site_name)
                fun.load_price(*clients_conf[site_name])
    else:
        print('Обработка сайта: ', site_name)
        fun.load_price(*clients_conf[site_name])


if __name__ == '__main__':
    main()