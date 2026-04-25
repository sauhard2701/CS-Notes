## Proxy

### Intent

Control access to another object.

### Class Diagram

There are four common kinds of proxy:

- Remote Proxy: controls access to a remote object in another address space. It encodes requests and parameters, then sends the encoded request to the object in the other address space.
- Virtual Proxy: creates expensive objects on demand. It can cache additional information about the real object to defer access to it. For example, when a website loads a large image that cannot be completed immediately, a virtual proxy can cache the image size and generate a temporary placeholder for the original image.
- Protection Proxy: controls access to an object based on permissions. It checks whether the caller has the access rights required to perform a request.
- Smart Reference: replaces a simple pointer and performs extra operations when accessing an object, such as counting references, loading the object into memory on first reference, and checking whether the real object is locked before access so other objects cannot modify it.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/9b679ff5-94c6-48a7-b9b7-2ea868e828ed.png"/> </div><br>

### Implementation

The following is a Virtual Proxy implementation. It simulates delayed image loading by using temporary content with the same size as the image until the image finishes loading.

```java
public interface Image {
    void showImage();
}
```

```java
public class HighResolutionImage implements Image {

    private URL imageURL;
    private long startTime;
    private int height;
    private int width;

    public int getHeight() {
        return height;
    }

    public int getWidth() {
        return width;
    }

    public HighResolutionImage(URL imageURL) {
        this.imageURL = imageURL;
        this.startTime = System.currentTimeMillis();
        this.width = 600;
        this.height = 600;
    }

    public boolean isLoad() {
        // 模拟图片加载，延迟 3s 加载完成
        long endTime = System.currentTimeMillis();
        return endTime - startTime > 3000;
    }

    @Override
    public void showImage() {
        System.out.println("Real Image: " + imageURL);
    }
}
```

```java
public class ImageProxy implements Image {

    private HighResolutionImage highResolutionImage;

    public ImageProxy(HighResolutionImage highResolutionImage) {
        this.highResolutionImage = highResolutionImage;
    }

    @Override
    public void showImage() {
        while (!highResolutionImage.isLoad()) {
            try {
                System.out.println("Temp Image: " + highResolutionImage.getWidth() + " " + highResolutionImage.getHeight());
                Thread.sleep(100);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        highResolutionImage.showImage();
    }
}
```

```java
public class ImageViewer {

    public static void main(String[] args) throws Exception {
        String image = "http://image.jpg";
        URL url = new URL(image);
        HighResolutionImage highResolutionImage = new HighResolutionImage(url);
        ImageProxy imageProxy = new ImageProxy(highResolutionImage);
        imageProxy.showImage();
    }
}
```

### JDK

- java.lang.reflect.Proxy
- RMI
