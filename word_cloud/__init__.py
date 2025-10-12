from wordcloud import WordCloud


class WordCloudGenerator(object):
    def __init__(self, github_repo):
        self._repo = github_repo

    def generate(self) -> str:
        if self._repo is None:
            print('self._repo is None')
            return ''

        frequencies = {}

        # get labels
        labels = self._repo.get_labels()
        print(labels)
        for label in labels:
            print(label)
            # 获取所有状态的 issues（包括 open 和 closed）
            issues_in_label = self._repo.get_issues(labels=(label.name,), state="all")
            # 实际计算 issues 数量，而不是使用 totalCount
            count = 0
            for issue in issues_in_label:
                count += 1
            frequencies[label.name] = count
            print(f"Label {label.name}: {count} issues")

        print(frequencies)
        
        # Check if all frequencies are zero to avoid division by zero error
        if not frequencies or all(freq == 0 for freq in frequencies.values()):
            print('No issues found with labels, skipping wordcloud generation')
            return 'assets/wordcloud.png'  # Return existing image path
        
        # generate wordcount image to local dir
        # specify the font to support Chinese word
        wc = WordCloud(font_path='lib/fonts/wqy-microhei.ttc', width=1920, height=400, background_color='white')
        wc.generate_from_frequencies(frequencies=frequencies)
        wc.to_file('assets/wordcloud.png')

        print('wordcloud picture generated successfully!')

        return 'assets/wordcloud.png'
