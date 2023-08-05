#!/usr/bin/env python
# -*- python-indent-offset: 4; -*-

import sys
import matplotlib
if matplotlib.get_backend() != "TKAgg":
    matplotlib.use("TKAgg")

import pmagpy.pmag as pmag
import pmagpy.pmagplotlib as pmagplotlib
import pmagpy.contribution_builder as cb
from pmag_env import set_env


def main():
    """
    NAME
        vgpmap_magic.py

    DESCRIPTION
        makes a map of vgps and a95/dp,dm for site means in a sites table

    SYNTAX
        vgpmap_magic.py [command line options]

    OPTIONS
        -h prints help and quits
        -eye  ELAT ELON [specify eyeball location], default is 90., 0.
        -f FILE sites format file, [default is sites.txt]
        -res [c,l,i,h] specify resolution (crude, low, intermediate, high]
        -etp plot the etopo20 topographpy data (requires high resolution data set)
        -prj PROJ,  specify one of the following:
             ortho = orthographic
             lcc = lambert conformal
             moll = molweide
             merc = mercator
        -sym SYM SIZE: choose a symbol and size, examples:
            ro 5 : small red circles
            bs 10 : intermediate blue squares
            g^ 20 : large green triangles
        -ell  plot dp/dm or a95 ellipses
        -rev RSYM RSIZE : flip reverse poles to normal antipode
        -S:  plot antipodes of all poles
        -age : plot the ages next to the poles
        -crd [g,t] : choose coordinate system, default is to plot all site VGPs
        -fmt [pdf, png, eps...] specify output format, default is pdf
        -sav  save and quit
    DEFAULTS
        FILE: sites.txt
        res:  c
        prj: ortho
        ELAT,ELON = 0,0
        SYM SIZE: ro 8
        RSYM RSIZE: g^ 8

    """
    if '-h' in sys.argv:
        print(main.__doc__)
        sys.exit()
    dir_path = pmag.get_named_arg("-WD", ".")
    # plot: default is 0, if -sav in sys.argv should be 1
    plot = pmag.get_flag_arg_from_sys("-sav", true=1, false=0)
    fmt = pmag.get_named_arg("-fmt", "pdf")
    res = pmag.get_named_arg("-res", "c")
    proj = pmag.get_named_arg("-prj", "ortho")
    anti = pmag.get_flag_arg_from_sys("-S", true=1, false=0)
    fancy = pmag.get_flag_arg_from_sys("-etp", true=1, false=0)
    ell = pmag.get_flag_arg_from_sys("-ell", true=1, false=0)
    ages = pmag.get_flag_arg_from_sys("-age", true=1, false=0)
    if '-rev' in sys.argv:
        flip = 1
        ind = sys.argv.index('-rev')
        rsym = (sys.argv[ind + 1])
        rsize = int(sys.argv[ind + 2])
    else:
        flip, rsym, rsize = 0, "g^", 8
    if '-sym' in sys.argv:
        ind = sys.argv.index('-sym')
        sym = (sys.argv[ind + 1])
        size = int(sys.argv[ind + 2])
    else:
        sym, size = 'ro', 8
    if '-eye' in sys.argv:
        ind = sys.argv.index('-eye')
        lat_0 = float(sys.argv[ind + 1])
        lon_0 = float(sys.argv[ind + 2])
    else:
        lat_0, lon_0 = 90., 0.
    crd = pmag.get_named_arg("-crd", "")
    coord_dict = {'g': 0, 't': 100}
    coord = coord_dict[crd] if crd else ""
    results_file = pmag.get_named_arg("-f", "sites.txt")

    con = cb.Contribution(dir_path, single_file=results_file)
    if not list(con.tables.keys()):
        print("-W - Couldn't read in data")
        return

    FIG = {'map': 1}
    pmagplotlib.plot_init(FIG['map'], 6, 6)
    # read in sites file
    lats, lons = [], []
    Pars = []
    dates, rlats, rlons = [], [], []

    site_container = con.tables['sites']
    site_container.front_and_backfill(['location'])
    site_df = site_container.df
    # use records with vgp_lat and vgp_lon
    if 'vgp_lat' in site_df.columns and 'vgp_lon' in site_df.columns:
        cond1, cond2 = site_df['vgp_lat'].notnull(), site_df['vgp_lon'].notnull()
    else:
        print ('nothing to plot')
        sys.exit()
    Results = site_df[cond1 & cond2]
    # use tilt correction
    if coord and 'dir_tilt_correction' in Results.columns:
        Results = Results[Results['dir_tilt_correction'] == coord]
    # get location name and average ages
    locs = Results['location'].dropna().unique()
    if len(locs):
        location = ":".join(Results['location'].unique())
    else:
        location = ""
    if 'age' in Results.columns and ages == 1:
        dates = Results['age'].unique()

    # go through rows and extract data
    for ind, row in Results.iterrows():
        lat, lon = float(row['vgp_lat']), float(row['vgp_lon'])
        if anti == 1:
            lats.append(-lat)
            lon = lon + 180.
            if lon > 360:
                lon = lon - 360.
            lons.append(lon)
        elif flip == 0:
            lats.append(lat)
            lons.append(lon)
        elif flip == 1:
            if lat < 0:
                rlats.append(-lat)
                lon = lon + 180.
                if lon > 360:
                    lon = lon - 360
                rlons.append(lon)
            else:
                lats.append(lat)
                lons.append(lon)

        ppars = []
        ppars.append(lon)
        ppars.append(lat)
        ell1, ell2 = "", ""
        if 'vgp_dm' in list(row.keys()) and row['vgp_dm']:
            ell1 = float(row['vgp_dm'])
        if 'vgp_dp' in list(row.keys()) and row['vgp_dp']:
            ell2 = float(row['vgp_dp'])
        if 'vgp_alpha95' in list(row.keys()) and (row['vgp_alpha95'] or row['vgp_alpha95'] == 0):
            ell1, ell2 = float(row['vgp_alpha95']), float(row['vgp_alpha95'])
        if ell1 and ell2:
            ppars = []
            ppars.append(lons[-1])
            ppars.append(lats[-1])
            ppars.append(ell1)
            ppars.append(lons[-1])
            try:
                isign = abs(lats[-1]) / lats[-1]
            except ZeroDivisionError:
                isign = 1
            ppars.append(lats[-1] - isign * 90.)
            ppars.append(ell2)
            ppars.append(lons[-1] + 90.)
            ppars.append(0.)
            Pars.append(ppars)

    location = location.strip(':')
    Opts = {'latmin': -90, 'latmax': 90, 'lonmin': 0., 'lonmax': 360.,
            'lat_0': lat_0, 'lon_0': lon_0, 'proj': proj, 'sym': 'bs',
            'symsize': 3, 'pltgrid': 0, 'res': res, 'boundinglat': 0.}
    Opts['details'] = {'coasts': 1, 'rivers': 0, 'states': 0,
                       'countries': 0, 'ocean': 1, 'fancy': fancy}
    # make the base map with a blue triangle at the pole
    pmagplotlib.plot_map(FIG['map'], [90.], [0.], Opts)
    Opts['pltgrid'] = -1
    Opts['sym'] = sym
    Opts['symsize'] = size
    if len(dates) > 0:
        Opts['names'] = dates
    if len(lats) > 0:
        # add the lats and lons of the poles
        pmagplotlib.plot_map(FIG['map'], lats, lons, Opts)
    Opts['names'] = []
    if len(rlats) > 0:
        Opts['sym'] = rsym
        Opts['symsize'] = rsize
        # add the lats and lons of the poles
        pmagplotlib.plot_map(FIG['map'], rlats, rlons, Opts)
    if plot == 0 and not set_env.IS_WIN:
        pmagplotlib.draw_figs(FIG)
    if ell == 1:  # add ellipses if desired.
        Opts['details'] = {'coasts': 0, 'rivers': 0, 'states': 0,
                           'countries': 0, 'ocean': 0, 'fancy': fancy}
        Opts['pltgrid'] = -1  # turn off meridian replotting
        Opts['symsize'] = 2
        Opts['sym'] = 'g-'
        for ppars in Pars:
            if ppars[2] != 0:
                PTS = pmagplotlib.plot_ell(FIG['map'], ppars, 'g.', 0, 0)
                elats, elons = [], []
                for pt in PTS:
                    elons.append(pt[0])
                    elats.append(pt[1])
                # make the base map with a blue triangle at the pole
                pmagplotlib.plot_map(FIG['map'], elats, elons, Opts)
                if plot == 0 and not set_env.IS_WIN:
                    pmagplotlib.draw_figs(FIG)
    files = {}
    for key in list(FIG.keys()):
        if pmagplotlib.isServer:  # use server plot naming convention
            files[key] = 'LO:_' + location + '_TY:_VGP_map.' + fmt
            con.add_magic_table('contribution')
            con_id = con.get_con_id()
            if con_id:
                files[key] = 'MC:_' + str(con_id) + '_' + files[key]
        else:  # use more readable naming convention
            files[key] = '{}_VGP_map.{}'.format(location, fmt)

    if pmagplotlib.isServer:
        black = '#000000'
        purple = '#800080'
        titles = {}
        titles['map'] = location + ' VGP map'
        FIG = pmagplotlib.add_borders(FIG, titles, black, purple)
        pmagplotlib.save_plots(FIG, files)
    elif plot == 0:
        pmagplotlib.draw_figs(FIG)
        ans = input(" S[a]ve to save plot, Return to quit:  ")
        if ans == "a":
            pmagplotlib.save_plots(FIG, files)
        else:
            print("Good bye")
            sys.exit()
    else:
        pmagplotlib.save_plots(FIG, files)


if __name__ == "__main__":
    main()
