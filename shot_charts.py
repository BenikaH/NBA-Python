import data_getters as dg
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
import seaborn as sns
import numpy as np
import urllib
from matplotlib.offsetbox import OffsetImage


def make_court_shapes():
    shapes = []

    outer_lines_shape = dict(
        type='rect',
        xref='x',
        yref='y',
        x0='-250',
        y0='-47.5',
        x1='250',
        y1='422.5',
        line=dict(
            color='rgba(10, 10, 10, 1)',
            width=1
        )
    )

    shapes.append(outer_lines_shape)

    hoop_shape = dict(
        type='circle',
        xref='x',
        yref='y',
        x0='7.5',
        y0='7.5',
        x1='-7.5',
        y1='-7.5',
        line=dict(
            color='rgba(10, 10, 10, 1)',
            width=1
        )
    )

    shapes.append(hoop_shape)

    backboard_shape = dict(
        type='rect',
        xref='x',
        yref='y',
        x0='-30',
        y0='-7.5',
        x1='30',
        y1='-6.5',
        line=dict(
            color='rgba(10, 10, 10, 1)',
            width=1
        ),
        fillcolor='rgba(10, 10, 10, 1)'
    )

    shapes.append(backboard_shape)

    outer_three_sec_shape = dict(
        type='rect',
        xref='x',
        yref='y',
        x0='-80',
        y0='-47.5',
        x1='80',
        y1='143.5',
        line=dict(
            color='rgba(10, 10, 10, 1)',
            width=1
        )
    )

    shapes.append(outer_three_sec_shape)

    inner_three_sec_shape = dict(
        type='rect',
        xref='x',
        yref='y',
        x0='-60',
        y0='-47.5',
        x1='60',
        y1='143.5',
        line=dict(
            color='rgba(10, 10, 10, 1)',
            width=1
        )
    )

    shapes.append(inner_three_sec_shape)

    left_line_shape = dict(
        type='line',
        xref='x',
        yref='y',
        x0='-220',
        y0='-47.5',
        x1='-220',
        y1='92.5',
        line=dict(
            color='rgba(10, 10, 10, 1)',
            width=1
        )
    )

    shapes.append(left_line_shape)

    right_line_shape = dict(
        type='line',
        xref='x',
        yref='y',
        x0='220',
        y0='-47.5',
        x1='220',
        y1='92.5',
        line=dict(
            color='rgba(10, 10, 10, 1)',
            width=1
        )
    )

    shapes.append(right_line_shape)

    three_point_arc_shape = dict(
        type='path',
        xref='x',
        yref='y',
        path='M -220 92.5 C -70 300, 70 300, 220 92.5',
        line=dict(
            color='rgba(10, 10, 10, 1)',
            width=1
        )
    )

    shapes.append(three_point_arc_shape)

    center_circle_shape = dict(
        type='circle',
        xref='x',
        yref='y',
        x0='60',
        y0='482.5',
        x1='-60',
        y1='362.5',
        line=dict(
            color='rgba(10, 10, 10, 1)',
            width=1
        )
    )

    shapes.append(center_circle_shape)

    res_circle_shape = dict(
        type='circle',
        xref='x',
        yref='y',
        x0='20',
        y0='442.5',
        x1='-20',
        y1='402.5',
        line=dict(
            color='rgba(10, 10, 10, 1)',
            width=1
        )
    )

    shapes.append(res_circle_shape)

    free_throw_circle_shape = dict(
        type='circle',
        xref='x',
        yref='y',
        x0='60',
        y0='200',
        x1='-60',
        y1='80',
        line=dict(
            color='rgba(10, 10, 10, 1)',
            width=1
        )
    )

    shapes.append(free_throw_circle_shape)

    res_area_shape = dict(
        type='circle',
        xref='x',
        yref='y',
        x0='40',
        y0='40',
        x1='-40',
        y1='-40',
        line=dict(
            color='rgba(10, 10, 10, 1)',
            width=1,
            dash='dot'
        )
    )

    shapes.append(res_area_shape)

    return shapes


def get_player_picture(player_id, player_name):
    file_path = '../player_pictures/' + player_name + '.png'
    if not dg.create_directories_and_check_for_file(file_path):
        pic = urllib.urlretrieve("http://stats.nba.com/media/players/230x185/" + str(player_id) + ".png",
                                 str(player_id) + ".png")
        player_pic = plt.imread(pic[0])
        plt.imsave(file_path, player_pic)
    else:
        player_pic = plt.imread(file_path)
    return player_pic


def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    # Diameter of a hoop is 18" so it has a radius of 9", which is a value
    # 7.5 in our coordinate system
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the
    # threes
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax


def make_matplot_scatter_shot_chart(df, player_name, player_id, year, season_type, chart_type):
    player_pic = get_player_picture(player_id, player_name)

    # create our jointplot
    joint_shot_chart = sns.jointplot(df.LOC_X, df.LOC_Y, stat_func=None, kind='scatter', space=0, alpha=0.5)

    joint_shot_chart.fig.set_size_inches(12, 11)

    # A joint plot has 3 Axes, the first one called ax_joint
    # is the one we want to draw our court onto and adjust some other settings
    ax = joint_shot_chart.ax_joint
    draw_court(ax)

    # Adjust the axis limits and orientation of the plot in order
    # to plot half court, with the hoop by the top of the plot
    ax.set_xlim(-250, 250)
    ax.set_ylim(422.5, -47.5)

    # Get rid of axis labels and tick marks
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.tick_params(labelbottom='off', labelleft='off')

    # Add a title
    ax.set_title(player_name + ' ' + dg.get_year_string(year) + ' ' + season_type,
                 y=1.2, fontsize=18)

    img = OffsetImage(player_pic, zoom=.7)
    img.set_offset((987, 907))
    ax.add_artist(img)

    file_path = '../charts/' + chart_type + '/scatter/' + player_name + '_' + str(
        year) + '_' + season_type + '.png'
    dg.create_directories_and_check_for_file(file_path)
    plt.savefig(file_path)
    plt.close()


def make_matplot_hexbin_shot_chart(df, player_name, player_id, year, season_type, chart_type):
    player_pic = get_player_picture(player_id, player_name)

    # create our jointplot

    cmap = plt.cm.coolwarm
    plt.axis([-250, 250, 422.5, -47.5])
    joint_shot_chart = sns.jointplot(df.LOC_X, df.LOC_Y, stat_func=None, reduce_C_function=np.sum,
                                     kind='hex', space=0, color=cmap(.2), cmap=cmap, extent=[-250, 250, 422.5, -47.5],
                                     gridsize=30)

    joint_shot_chart.fig.set_size_inches(12, 11)

    # A joint plot has 3 Axes, the first one called ax_joint
    # is the one we want to draw our court onto
    ax = joint_shot_chart.ax_joint
    draw_court(ax)

    # Adjust the axis limits and orientation of the plot in order
    # to plot half court, with the hoop by the top of the plot
    ax.set_xlim(-250, 250)
    ax.set_ylim(422.5, -47.5)

    # Get rid of axis labels and tick marks
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.tick_params(labelbottom='off', labelleft='off')

    # Add a title
    ax.set_title(player_name + ' ' + dg.get_year_string(year) + ' ' + season_type,
                 y=1.2, fontsize=18)

    img = OffsetImage(player_pic, zoom=0.6)
    img.set_offset((987, 907))
    ax.add_artist(img)

    file_path = '../charts/' + chart_type + '/hexbin/' + player_name + '_' + str(
        year) + '_' + season_type + '.png'
    dg.create_directories_and_check_for_file(file_path)
    plt.savefig(file_path)
    plt.close()


def make_matplot_kde_shot_chart(df, player_name, player_id, year, season_type, chart_type):
    player_pic = get_player_picture(player_id, player_name)

    # create our jointplot

    # get our colormap for the main kde plot
    # Note we can extract a color from cmap to use for
    # the plots that lie on the side and top axes
    cmap = plt.cm.viridis

    # n_levels sets the number of contour lines for the main kde plot
    joint_shot_chart = sns.jointplot(df.LOC_X, df.LOC_Y, stat_func=None,
                                     kind='kde', space=0, color=cmap(0.1),
                                     cmap=cmap, n_levels=50, extent=[-250, 250, 422.5, -47.5])

    joint_shot_chart.fig.set_size_inches(12, 11)

    # A joint plot has 3 Axes, the first one called ax_joint
    # is the one we want to draw our court onto and adjust some other settings
    ax = joint_shot_chart.ax_joint
    draw_court(ax)

    # Adjust the axis limits and orientation of the plot in order
    # to plot half court, with the hoop by the top of the plot
    ax.set_xlim(-250, 250)
    ax.set_ylim(422.5, -47.5)

    # Get rid of axis labels and tick marks
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.tick_params(labelbottom='off', labelleft='off')

    # Add a title
    title = player_name + ' ' + dg.get_year_string(year) + ' ' + season_type
    ax.set_title(title,
                 y=1.2, fontsize=18)

    # Add Data Scource and Author
    ax.text(-250, 445, 'Data Source: stats.nba.com',
            fontsize=12)

    # Add Harden's image to the top right
    # First create our OffSetImage by passing in our image
    # and set the zoom level to make the image small enough
    # to fit on our plot
    img = OffsetImage(player_pic, zoom=0.6)
    # Pass in a tuple of x,y coordinates to set_offset
    # to place the plot where you want, I just played around
    # with the values until I found a spot where I wanted
    # the image to be
    img.set_offset((987, 907))
    # add the image
    ax.add_artist(img)

    file_path = '../charts/' + chart_type + '/kde/' + player_name + '_' + str(
        year) + '_' + season_type + '.png'
    dg.create_directories_and_check_for_file(file_path)
    plt.savefig(file_path)
    plt.close()


def make_histogram(df, player_name, year, season_type, chart_type):
    plt.figure()
    title = player_name + ' ' + dg.get_year_string(year) + ' ' + season_type
    plt.title(title)
    plt.xlabel('Distance (Feet)')
    df['SHOT_DISTANCE'].plot.hist(alpha=0.5)
    file_path = '../charts/' + chart_type + '/hist/' + player_name + '_' + str(year) + '_' + season_type + '.png'
    dg.create_directories_and_check_for_file(file_path)
    plt.savefig(file_path)
    plt.close()
