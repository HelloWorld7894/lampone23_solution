import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib
matplotlib.use("TkAgg")

def visualization(original_img,detect_playground_img,detect_robot_img,recognize_objects_img,analyze_playground,path):
    fig, axs = plt.subplots(2, 3, figsize=(15, 10))
    axs[0][0].imshow(original_img)
    axs[0][0].set_title('orichinal')
    axs[0][1].imshow(detect_playground_img)
    axs[0][1].set_title('playground_detection')
    axs[0][2].imshow(detect_robot_img)
    axs[0][2].set_title('robot_detection')
    axs[1][0].imshow(recognize_objects_img)
    axs[1][0].set_title('Recognize_objects')
    #visualization of 2d np aray
    colors = ['white', 'black', 'green', 'blue', 'red','orange']
    cmap = ListedColormap(colors)
    axs[1][1].imshow(analyze_playground, cmap=cmap)
    axs[1][1].set_title('8x8 Array')
    plt.tight_layout()
    plt.show()