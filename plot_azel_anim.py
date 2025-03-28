# %% [markdown]
# # Az/El plot for Subaru observations

# %% [markdown]
# ### hacked from https://docs.astropy.org/en/stable/generated/examples/coordinates/plot_obs-planning.html

# %%
import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
import pandas as pd
from matplotlib.pyplot import cm
from astropy.visualization import astropy_mpl_style, quantity_support
plt.style.use(astropy_mpl_style)
quantity_support()
%matplotlib inline
from IPython.display import display, HTML
from matplotlib.animation import FuncAnimation


# %%
# load source coordinates from target list (csv file)
sourcelist = pd.read_csv('/Users/mariavincent/GitHub_Repos/get_targets/disk_survey_data/S25B-Targets.csv')
sourcelist

# %% [markdown]
# ## Go through Source List

# %%
sourcelist_final = sourcelist

sourcelist_final = sourcelist_final.reset_index()
sources = sourcelist['Target']
coords = [SkyCoord(ra * u.deg, dec * u.deg, frame='icrs') 
          for ra, dec in zip(sourcelist['RA'], sourcelist['Decl'])]

# %% [markdown]
# ## Set up observing params

# %%
# Observing run on Subaru the night of 12/27/22
dates = pd.date_range(start='2025-08-01', end='2026-01-31', freq='D')
Subaru = EarthLocation.of_site('Subaru')
utcoffset = -10*u.hour  # Hawaii Standard Time relative to UT
midnights = Time(dates) - utcoffset

# %%
from astropy.coordinates import get_sun
delta_midnight = np.linspace(-12, 12, 1000)*u.hour
# midnight = Time('2022-4-02 00:00:00') - utcoffset
# night = midnight + delta_midnight
nights = midnights
sun_altazs_nights =[]
for night in nights:
    night += delta_midnight
    night_frame = AltAz(obstime=night, location=Subaru)
    sun_altazs_night = get_sun(night).transform_to(night_frame)
    sun_altazs_nights.append(sun_altazs_night)

# %%
# this might take a while the first time you run since it downloads a ~10MB file
from astropy.coordinates import get_body
moon_altazs_nights =[]
nights = midnights
for night in nights:
    night += delta_midnight
    night_frame = AltAz(obstime=night, location=Subaru)
    moon_night = get_body('moon', night).transform_to(night_frame)
    moon_altazs_nights.append(moon_night)


# %% [markdown]
# ## Plot

# %%
from matplotlib.animation import FuncAnimation

# Alt vs time plot
fig = plt.figure(figsize=(14,8))
ax = fig.add_subplot(111)
ax.set_xlabel('Hours from HST Midnight')
ax.set_ylabel('Altitude [deg]')

# Function to update the plot for each frame
def update(frame):
    ax.clear()
    ax.set_xlabel('Hours from HST Midnight')
    ax.set_ylabel('Altitude [deg]')
    ax.set_xlim(-8*u.hour, 8*u.hour)
    ax.set_xticks((np.arange(9)*2-8)*u.hour)
    ax.set_ylim(0*u.deg, 90*u.deg)

    # Update Sun and Moon
    ax.plot(delta_midnight, sun_altazs_nights[frame].alt, lw=2, color='orange', ls='--', label='Sun')
    ax.plot(delta_midnight, moon_altazs_nights[frame].alt, lw=2, color='white', alpha=0.5, ls='--', label='Moon')

    # Update each source
    color = cm.magma(np.linspace(0.4, 1, len(sources)))
    for i, s in enumerate(sources):
        night = midnights[frame] + delta_midnight
        night_frame = AltAz(obstime=night, location=Subaru)
        source_altazs_night = coords[i].transform_to(night_frame)
        ax.plot(delta_midnight, source_altazs_night.alt, label=s,  ls='--', color=color[i])

    # Twilight and night shading
    ax.fill_between(delta_midnight, 0*u.deg, 90*u.deg,
                    sun_altazs_nights[frame].alt < -0*u.deg, color='0.5', zorder=0)
    ax.fill_between(delta_midnight, 0*u.deg, 90*u.deg,
                    sun_altazs_nights[frame].alt < -18*u.deg, color='k', zorder=0)
    
    # Title
    ax.set_title(dates[frame].strftime('%Y-%m-%d'))

    # Legend
    legend = ax.legend(loc='upper left', frameon=1)
    frame = legend.get_frame()
    frame.set_facecolor('gray')

# Create animation
ani = FuncAnimation(fig, update, frames=len(midnights), repeat=False)
HTML(ani.to_jshtml())
# plt.show()

# %%
# # Sun and Moon
# ax.plot(delta_midnight, sun_altazs_night.alt, lw=2, color='orange', ls='--', label='Sun')
# # ax.plot(delta_midnight, moon_altazs_night.alt, lw=2, color='white', alpha=0.5, ls='--', label='Moon')

# # each source
# color = cm.tab10(np.linspace(0, 1, len(sources)))
# nc = 0
# for i,s in enumerate(sources):
#     # if sourcelist['Priority'][i] == 99:
#     source_altazs_night = coords[i].transform_to(night_frame)
#     ax.scatter(delta_midnight, source_altazs_night.alt,label=s, s=20, color=color[nc])
#     nc += 1
#     # print(i,s)

# # twilight
# ax.fill_between(delta_midnight, 0*u.deg, 90*u.deg,
#                  sun_altazs_night.alt < -0*u.deg, color='0.5', zorder=0)
# # night
# ax.fill_between(delta_midnight, 0*u.deg, 90*u.deg,
#                  sun_altazs_night.alt < -18*u.deg, color='k', zorder=0)

# #plt.colorbar().set_label('Azimuth [deg]')

# legend = plt.legend(loc='upper left', frameon=1)
# frame = legend.get_frame()
# frame.set_facecolor('gray')

# #ax.set_xlim(-12*u.hour, 12*u.hour)
# #ax.set_xticks((np.arange(13)*2-12)*u.hour)
# ax.set_xlim(-8*u.hour, 8*u.hour)
# ax.set_xticks((np.arange(9)*2-8)*u.hour)
# ax.set_ylim(0*u.deg, 90*u.deg)


# # plt.savefig("azel_041523.png", dpi=300)

# %%



