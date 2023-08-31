import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib
matplotlib.use("TkAgg")

def visualization(original_img,detect_playground_img,detect_robot_img,recognize_objects_img,analyze_playground,path_img,animIMG):
    fig, axs = plt.subplots(2, 4, figsize=(15, 10))
    colors = ['white', 'black', 'green', 'blue', 'red','orange']
    cmap = ListedColormap(colors)
    colors = ['white', 'black', 'green', 'black', 'blue','black','blue','gray']
    cmap_path = ListedColormap(colors)
    axs[0][0].imshow(original_img)
    axs[0][0].set_title('orichinal')
    axs[0][1].imshow(detect_playground_img)
    axs[0][1].set_title('playground_detection')
    axs[0][2].imshow(detect_robot_img)
    axs[0][2].set_title('robot_detection')
    axs[0][3].imshow(recognize_objects_img)
    axs[0][3].set_title('Recognize_objects')
    #visualization of 2d np aray
    axs[1][0].imshow(analyze_playground, cmap=cmap)
    axs[1][0].set_title('8x8 Array')
    #visualization of path
    axs[1][1].imshow(path_img, cmap=cmap_path)
    axs[1][1].set_title('PATH')
    
    axs[1][2].imshow(animIMG)
    axs[1][2].set_title('Animation')
    plt.tight_layout()
    plt.show()