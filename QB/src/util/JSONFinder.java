package util;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class JSONFinder {
    public static String get(String key) {
        String regex = "\"" + key + "\": \".*\"";
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(key);
        if (matcher.find()) {
            return matcher.group();
        }
        return null;
    }
}
