/**
 * Markdown 渲染器
 * 使用 marked.js 渲染 Markdown，使用 highlight.js 高亮代码
 */

(function() {
    'use strict';
    
    // 配置 marked 选项（GitHub 风格）
    if (typeof marked !== 'undefined') {
        marked.setOptions({
            gfm: true,
            breaks: true,
            headerIds: true,
            mangle: false
        });
    }
    
    /**
     * 自定义渲染器处理代码高亮
     */
    function createCustomRenderer() {
        const renderer = new marked.Renderer();
        
        // 自定义代码块渲染
        renderer.code = function(code, language) {
            if (language && typeof hljs !== 'undefined' && hljs.getLanguage(language)) {
                try {
                    const highlighted = hljs.highlight(code, { language: language }).value;
                    return `<pre><code class="hljs language-${language}">${highlighted}</code></pre>`;
                } catch (e) {
                    console.warn('代码高亮失败:', e);
                }
            }
            // 自动检测语言
            if (typeof hljs !== 'undefined') {
                try {
                    const highlighted = hljs.highlightAuto(code).value;
                    return `<pre><code class="hljs">${highlighted}</code></pre>`;
                } catch (e) {
                    console.warn('代码自动高亮失败:', e);
                }
            }
            return `<pre><code>${code}</code></pre>`;
        };
        
        // 自定义标题渲染（添加 ID）
        renderer.heading = function(text, level) {
            // 生成简单的 slug
            const slug = text
                .toLowerCase()
                .replace(/[^\w\u4e00-\u9fff\s-]/g, '')
                .replace(/\s+/g, '-')
                .replace(/-+/g, '-')
                .trim();
            
            return `<h${level} id="${slug}">${text}</h${level}>`;
        };
        
        return renderer;
    }
    
    /**
     * 渲染 Markdown
     */
    function renderMarkdown() {
        const markdownScript = document.getElementById('article-markdown');
        const contentDiv = document.getElementById('markdown-content');
        
        if (!markdownScript || !contentDiv) {
            console.warn('未找到 Markdown 容器元素');
            return;
        }
        
        try {
            // 解析 JSON 数据
            const markdown = JSON.parse(markdownScript.textContent);
            
            if (!markdown) {
                console.warn('Markdown 内容为空');
                return;
            }
            
            // 创建自定义渲染器
            const renderer = createCustomRenderer();
            
            // 渲染 Markdown
            const html = marked.parse(markdown, { renderer: renderer });
            contentDiv.innerHTML = html;
            
            console.log('Markdown 渲染完成');
            
            // 生成 TOC
            generateTOC();
            
        } catch (e) {
            console.error('Markdown 渲染失败:', e);
            contentDiv.innerHTML = `<p style="color: red;">渲染失败: ${e.message}</p>`;
        }
    }
    
    /**
     * 生成目录
     */
    function generateTOC() {
        const content = document.getElementById('markdown-content');
        const tocContainer = document.getElementById('toc-container');
        const tocList = document.getElementById('toc-list');
        const articleLayout = document.querySelector('.article-layout');
        
        if (!content || !tocContainer || !tocList) {
            console.warn('未找到 TOC 容器元素');
            return;
        }
        
        const headings = content.querySelectorAll('h1, h2, h3, h4, h5, h6');
        
        if (headings.length === 0) {
            tocContainer.style.display = 'none';
            articleLayout.classList.remove('has-toc');
            // 添加无目录文章页类名
            document.body.classList.add('page-article-no-toc');
            document.body.classList.remove('page-article-with-toc');
            console.log('文章没有标题，隐藏 TOC');
            return;
        }
        
        // 有目录时添加类名
        articleLayout.classList.add('has-toc');
        // 添加有目录文章页类名
        document.body.classList.add('page-article-with-toc');
        document.body.classList.remove('page-article-no-toc');
        
        // 清空现有 TOC
        tocList.innerHTML = '';
        
        // 为每个标题创建 TOC 项
        headings.forEach((heading, index) => {
            // 确保标题有 ID
            if (!heading.id) {
                heading.id = `heading-${index}`;
            }
            
            const li = document.createElement('li');
            const level = parseInt(heading.tagName[1]);
            li.className = `toc-item level-${level}`;
            
            const a = document.createElement('a');
            a.href = `#${heading.id}`;
            a.textContent = heading.textContent;
            
            // 添加平滑滚动
            a.addEventListener('click', function(e) {
                e.preventDefault();
                heading.scrollIntoView({ behavior: 'smooth', block: 'start' });
            });
            
            li.appendChild(a);
            tocList.appendChild(li);
        });
        
        console.log(`TOC 生成完成，共 ${headings.length} 个标题`);
        
        // 初始化 TOC 滚动高亮
        initTOCScrollHighlight(headings);
    }
    
    /**
     * 初始化 TOC 滚动高亮
     */
    function initTOCScrollHighlight(headings) {
        if (headings.length === 0) return;
        
        let ticking = false;
        
        function updateActiveTocItem() {
            const scrollTop = window.pageYOffset;
            let currentHeading = null;
            
            // 找到当前滚动位置对应的标题
            headings.forEach(heading => {
                const headingTop = heading.offsetTop - 100; // 偏移量
                if (scrollTop >= headingTop) {
                    currentHeading = heading;
                }
            });
            
            // 更新 TOC 项激活状态
            const tocItems = document.querySelectorAll('.toc-item');
            tocItems.forEach(item => item.classList.remove('active'));
            
            if (currentHeading) {
                const activeLink = document.querySelector(`.toc-item a[href="#${currentHeading.id}"]`);
                if (activeLink) {
                    activeLink.parentElement.classList.add('active');
                }
            }
        }
        
        // 节流滚动监听
        window.addEventListener('scroll', function() {
            if (!ticking) {
                requestAnimationFrame(function() {
                    updateActiveTocItem();
                    ticking = false;
                });
                ticking = true;
            }
        });
        
        // 初始调用
        updateActiveTocItem();
    }
    
    // 页面加载时渲染
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', renderMarkdown);
    } else {
        // DOM 已经加载完成
        renderMarkdown();
    }
})();

