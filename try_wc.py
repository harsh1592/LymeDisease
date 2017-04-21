import matplotlib.pyplot as plt
import sys

from wordcloud import WordCloud, STOPWORDS

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % 0

def build_wordcloud(input_file,output_file):

    text = open(input_file).read()
    
    stopwords = set(STOPWORDS)
    stopwords.add("LYME")
    stopwords.add("lyme")
    wc = WordCloud(max_words=1000000, background_color="white", width=1024,
     height=768, stopwords=stopwords, margin=2,
                   random_state=1).generate(text)
    plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3),
               interpolation="bilinear")
    wc.to_file(output_file)
    plt.axis("off")    

def main():
    build_wordcloud(str(sys.argv[1]),str(sys.argv[2]))
    
if __name__ == '__main__':
    main()