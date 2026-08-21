merged_dir = '/Users/yinuo/Desktop/Apep/Apep_JWST_2024/Merged_for_colour/'

style_plots('in, w')
plt.rc('font', family='Serif', size=8)


## Read in images
im_770 = read(merged_dir + 'Im_merged_log_rot_cut_770.fits')
im_1500 = read(merged_dir + 'Im_merged_log_rot_cut_1500.fits')
im_2550 = read(merged_dir + 'Im_merged_log_rot_cut_2550.fits')


## Plot
# b = np.clip(im_770, 1, 3.76) - 1
# g = np.clip(im_1500, 0.7, 3.9) - 0.7
# r = np.clip(im_2550, 1.6, 4.3) - 1.6

b = np.clip(im_770, 1, 4.0) - 1
g = np.clip(im_1500, 0.7, 3.9) - 0.7
r = np.clip(im_2550, 1.6, 4.5) - 1.6

b = b / b.max()
g = g / g.max()
r = r / r.max()

def transform(im, grid):
    regular_grid = np.linspace(grid[0], grid[-1], len(grid))
    im = np.interp(im, grid, regular_grid)
    return im
    # y, x = im.shape
    # for j in range(y):
    #     for i in range(x):
    #         im[j, i] = np.interp(im[j, i], grid, regular_grid)

b_orig = b.copy()
g_orig = g.copy()
r_orig = r.copy()

b = transform(b_orig, [0, 0.05, 0.10, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 1.0])
g = transform(g_orig, [0, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0])
r = transform(r_orig, [0, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0])

gvar = transform(g_orig, [0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

b = b / b.max() * 1
g = g / g.max() * 1
r = r / r.max() * 1

# norm = np.max([r, g, b])
# b = b / norm
# g = g / norm
# r = r / norm

if 0:
    fig, ax = plt.subplots(1, 3, figsize=(18, 7))
    ax[0].imshow(b, origin='lower', clim=[0, 1])
    ax[1].imshow(gvar, origin='lower', clim=[0, 1])
    ax[2].imshow(r, origin='lower', clim=[0, 1])
    plt.show()


# RGB image
#image = np.stack([r, b, b], axis=-1)
#image = np.stack([r * 1.1, g, b * 1.4], axis=-1)

# Use this one
image = np.stack([r * 1.4, gvar * 0.3 + b * 0.8, b*1.4], axis=-1)

#image = np.stack([r * 1.1, b, b * 1.4], axis=-1)
#image = np.stack([r * 1.2, g*0.3 + b*0.7, b * 1.4], axis=-1)

ydim, xdim = r.shape
cy, cx = 400, 522
scale = 0.11 # arcsec/pixel
extent = np.array([cx, -(xdim - cx), -cy, ydim - cy]) * scale

fig, ax = plt.subplots()
plt.imshow(image, origin='lower', extent=extent)
plt.xlabel('Relative RA (arcsec)')
plt.ylabel('Relative Dec (arcsec)')

def arcsec_to_au(x):
    return 2.4e3 * x / 1e3

def au_to_arcsec(x):
    return x / 2.4e3 / 1e3

ax_top = ax.secondary_xaxis('top', functions=(arcsec_to_au, au_to_arcsec))
ax_right = ax.secondary_yaxis('right', functions=(arcsec_to_au, au_to_arcsec))

ax_right.set_ticks([-100, -50, 0, 50, 100])

ax.minorticks_on()
ax_top.minorticks_on()
ax_right.minorticks_on()

ax_top.set_xlabel(r'Displacement (kau)')
ax_right.set_ylabel(r'Displacement (kau)')

"Label North"
plt.arrow(x=52, y=36, dx=0, dy=5, color='w', lw=0.5, alpha=0.6, head_width=1, head_length=1)
plt.text(52, 42.5, 'N', color='w', alpha=0.8, fontsize=6, ha='center', va='bottom')

#plt.axis('off')

plt.show()


## Get VISIR colour image
"Run /Users/yinuo/Desktop/Apep/Apep_VISIR_2024/colour_image.py"
if 0:
    visir_image = image


## Add VISIR image as inset
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib

ydim, xdim, _ = visir_image.shape
cy, cx = 199.5, 199.5
scale = 0.045 # arcsec/pixel
extent = np.array([xdim - cx, -cx, -cy, ydim - cy]) * scale

matplotlib.rc('axes', edgecolor='w', lw=0.25)

inset_size = 0.8
axins = inset_axes(ax, width=inset_size, height=inset_size)
axins.imshow(visir_image, origin='lower', extent=extent)
axins.set_xticks([-5, 0, 5])
axins.set_xticks([-5, 0, 5])

axins.tick_params(width=0.25)
axins.tick_params(length=2)
axins.tick_params(top=True, bottom=True, left=True, right=True)

axins.set_xticklabels([])
axins.set_yticklabels([])

if 0:
    plt.savefig('/Users/yinuo/Desktop/Apep/figures/colour_arrow.pdf', bbox_inches='tight')
