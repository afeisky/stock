import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Timer;
import java.util.UUID;

public class SinaDownLoad {
	private static String url = "http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/600000.phtml?year=2014&jidu=1";

	public static boolean saveUrlAs(String photoUrl, String fileName) {
		// only support HTTP:
		try {
			URL url = new URL(photoUrl);
			HttpURLConnection connection = (HttpURLConnection) url
					.openConnection();
			DataInputStream in = new DataInputStream(
					connection.getInputStream());
			DataOutputStream out = new DataOutputStream(new FileOutputStream(
					fileName));
			System.out.println("fileName: " + fileName);
			byte[] buffer = new byte[4096];
			int count = 0;
			while ((count = in.read(buffer)) > 0) {
				out.write(buffer, 0, count);
			}
			out.close();
			in.close();
			return true;
		} catch (Exception e) {
			return false;
		}
	}

	public String getDocumentAt(String urlString) {
		// HTTP,FTP
		StringBuffer document = new StringBuffer();
		try {
			URL url = new URL(urlString);
			URLConnection conn = url.openConnection();
			BufferedReader reader = new BufferedReader(new InputStreamReader(
					conn.getInputStream()));
			String line = null;
			while ((line = reader.readLine()) != null) {
				document.append(line + "/n");
			}
			reader.close();
		} catch (MalformedURLException e) {
			System.out.println("Unable to connect to URL: " + urlString);
		} catch (IOException e) {
			System.out.println("IOException when connecting to URL: "
					+ urlString);
		}
		return document.toString();
	}

	static private void sendMsessageInNewThread() {
		new Thread(new Runnable() {
			@Override
			public void run() {
				Message msg = new Message();
				System.out.println("sup thread "
						+ Thread.currentThread().getName()
						+ ": send message------");
				handler.sendMessage(msg);
			}
		}).start();
	}


	private static boolean haveFailDownload=false;
	private static int haveFailDownload_count=0;
	static private int download_do(){
		String appRootDir = System.getProperty("user.dir");
		String str = list.get(iList);
		String[] strArray = str.split("  ");
		String downloadUrl;
		String downloadFileName;
		if (strArray.length == 2) {
			downloadUrl = strArray[0];
			downloadFileName = Paths.get(appRootDir, PATH_NAME, strArray[1]).toString();	
		} else {
			downloadUrl = strArray[0];
			downloadFileName = Paths.get(appRootDir, PATH_NAME,  head + Integer.valueOf(iList)+ ".htm").toString();	
		}
		//filename=downloadUrl.substring(downloadUrl.lastIndexOf("/"));
		
		File f=new File(downloadFileName);
		System.out.println(downloadUrl+", "+downloadFileName+";"+f.length());
		int flag=0;
		//if (f.length()<20000){
		//	f.delete();
		//	System.out.println("delete,");
		//}
		
		if (f.length()<30000){//(!f.exists()){
			System.out.println("-->");
			if (saveUrlAs(downloadUrl, downloadFileName)) {
				flag=1;
			}else{
				flag=2;
			}
		}
		if ((flag==1) || f.length()<30000){
			System.out.println("[" + iList+"/"+list.size()+"] Error: fail download: "+downloadUrl);
			haveFailDownload=true;
		}
		return flag;
	}
	static private void download_sendMsg() {
		System.out.println("[" + iList+"/"+list.size()+"]");	
		Message msg = new Message();
		msg.what = 1;
		//System.out.println("thread " + Thread.currentThread().getName()+ ": send message--" + Integer.valueOf(count));
		handler.sendMessage(msg);
	}	
	static Handler handler = null;
	
	static private void download_main() {
		Looper.prepare();
		handler = new Handler() {
			@Override
			public void handleMessage(Message msg) {
				if (msg.what == 1) {
					int flag=download_do();
					try {
						if (flag>0){
							Thread.sleep(1500);
						}
					} catch (InterruptedException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
					iList++;
					if (iList<(list.size())){							
						download_sendMsg();
					}else{
						System.out.println("============ Next "+Integer.valueOf(haveFailDownload_count)+"======================");	
						if (haveFailDownload) {
							iList=0;
							haveFailDownload=false;
							haveFailDownload_count++;
							download_sendMsg();
						}
					}
				}
			}
		};
		download_sendMsg();
		Looper.loop();
	}

	private static int count = 0;

	static private void demo() {
		Looper.prepare();
		final Handler handler = new Handler() {
			@Override
			public void handleMessage(Message msg) {
				System.out.println("main thread recv message------"
						+ Integer.valueOf(msg.what) + "," + msg.obj.toString());
			}
		};

		for (int i = 0; i < 10; i++) {
			new Thread(new Runnable() {
				@Override
				public void run() {
					Message msg = new Message();
					synchronized (UUID.class) {
						msg.obj = UUID.randomUUID().toString();
					}
					count++;
					msg.what = 1;
					System.out.println(Integer.valueOf(count) + " sup thread "
							+ Thread.currentThread().getName()
							+ ": send message------" + msg.obj);
					handler.sendMessage(msg);
				}
			}).start();
		}
		Looper.loop();
	}

	private static void readUrlFile() {
		String appRootDir = System.getProperty("user.dir");
		Path path = Paths.get(appRootDir, PATH_NAME, "downloadin.txt");		
		String inFileName = path.toString();
		System.out.println(inFileName);
		try {
			StringBuffer sb = new StringBuffer("");
			FileReader reader = new FileReader(inFileName);
			BufferedReader br = new BufferedReader(reader);
			String str = null;

			while ((str = br.readLine()) != null) {
				// sb.append(str+"/n");
				list.add(str);
				//System.out.println(str);
			}
			br.close();
			reader.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}

	}

	static List<String> list = new ArrayList<String>();
	private static int iList = 0;
	private static String PATH_NAME = "DownloadData";
	private static String head = "DL";

	public static void go(String[] args) {
		String appRootDir = System.getProperty("user.dir");
		System.out.println("== " + appRootDir);
		readUrlFile();
		download_main();
	}

}
