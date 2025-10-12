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
            issues_in_label = self._repo.get_issues(labels=[str(label.name)], state="all")
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
        
        # generate wordcount images to local dir
        # specify the font to support Chinese word
        
        # Generate light theme version (white background, dark text)
        wc_light = WordCloud(
            font_path='lib/fonts/wqy-microhei.ttc', 
            width=1920, 
            height=400, 
            background_color='white',
            colormap='viridis'
        )
        wc_light.generate_from_frequencies(frequencies=frequencies)
        wc_light.to_file('assets/wordcloud-light.png')
        
        # Generate dark theme version (dark background, light text)
        wc_dark = WordCloud(
            font_path='lib/fonts/wqy-microhei.ttc', 
            width=1920, 
            height=400, 
            background_color='#1a1a1a',
            colormap='plasma',
            relative_scaling=0.5
        )
        wc_dark.generate_from_frequencies(frequencies=frequencies)
        wc_dark.to_file('assets/wordcloud-dark.png')
        
        # Keep backward compatibility - copy light version to old filename
        wc_light.to_file('assets/wordcloud.png')

        print('wordcloud pictures generated successfully!')

        return 'assets/wordcloud-light.png'
