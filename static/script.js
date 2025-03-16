document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const generateBtn = document.getElementById('generate-btn');
    const clearBtn = document.getElementById('clear-btn');
    const promptInput = document.getElementById('prompt-input');
    const loadingElement = document.getElementById('loading');
    const resultsElement = document.getElementById('results');
    const planOutput = document.getElementById('plan-output');
    const codeOutput = document.getElementById('code-output');
    const debugOutput = document.getElementById('debug-output');
    const debugPlanOutput = document.getElementById('debug-plan-output');
    const completeCodeOutput = document.getElementById('complete-code-output');
    const validationOutput = document.getElementById('validation-output');
    
    // Tab functionality with animation
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Add transition effect
            tabPanes.forEach(pane => {
                if (pane.classList.contains('active')) {
                    pane.style.opacity = '0';
                    setTimeout(() => {
                        pane.classList.remove('active');
                    }, 300);
                }
            });
            
            // Deactivate all tabs
            tabButtons.forEach(btn => btn.classList.remove('active'));
            
            // Activate the clicked tab
            button.classList.add('active');
            const tabId = button.getAttribute('data-tab');
            
            setTimeout(() => {
                const activePane = document.getElementById(tabId);
                activePane.classList.add('active');
                setTimeout(() => {
                    activePane.style.opacity = '1';
                }, 50);
            }, 300);
        });
    });
    
    // Make primary buttons more interactive
    const primaryButtons = document.querySelectorAll('.primary-btn');
    primaryButtons.forEach(button => {
        // Wrap text in span for positioning
        const buttonText = button.textContent;
        button.innerHTML = `<span>${buttonText}</span>`;
        
        // Add ripple effect
        button.addEventListener('mousedown', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            ripple.style.cssText = `
                position: absolute;
                background: rgba(255, 255, 255, 0.15);
                border-radius: 50%;
                width: 100px;
                height: 100px;
                left: ${x - 50}px;
                top: ${y - 50}px;
                transform: scale(0);
                pointer-events: none;
                animation: ripple 0.6s linear;
            `;
            
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
    
    // Add keyframes for ripple effect
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Process code to extract file structure
    function processCompleteCode(codeString) {
        // Look for common file patterns in the code
        const filePatterns = [
            {regex: /```(?:html|)\s*(?:<.*?>)?\s*<!DOCTYPE html>/i, language: 'html', filename: 'index.html'},
            {regex: /```(?:css|)\s*(?:<.*?>)?\s*(?:\/\*.*?\*\/\s*)?(?:body|html|\*|:root)/i, language: 'css', filename: 'styles.css'},
            {regex: /```(?:js|javascript)\s*(?:<.*?>)?\s*(?:\/\/.*?\n|\/\*.*?\*\/\s*)?(?:function|const|let|var|import|document)/i, language: 'javascript', filename: 'script.js'},
            {regex: /```(?:py|python)\s*(?:<.*?>)?\s*(?:#.*?\n|"""|''')?(?:import|from|def|class)/i, language: 'python', filename: 'app.py'},
            {regex: /```(?:java)\s*(?:<.*?>)?\s*(?:\/\/.*?\n|\/\*.*?\*\/\s*)?(?:public class|class|import|package)/i, language: 'java', filename: 'Main.java'}
        ];
        
        // Split by code blocks
        const codeBlocks = codeString.split(/```(?:\w*)/);
        let formattedCode = '';
        let inCodeBlock = false;
        let currentLanguage = '';
        
        // Process the code to identify files
        codeBlocks.forEach((block, index) => {
            if (index === 0) return; // Skip first split which is usually introduction text
            
            if (!inCodeBlock) {
                // We're at the start of a code block, try to identify the file
                let fileIdentified = false;
                
                for (const pattern of filePatterns) {
                    if (pattern.regex.test('```' + block)) {
                        formattedCode += `\n### File: ${pattern.filename}\n\n\`\`\`${pattern.language}\n`;
                        currentLanguage = pattern.language;
                        fileIdentified = true;
                        break;
                    }
                }
                
                if (!fileIdentified) {
                    // If we can't identify, use a generic filename based on the language
                    const langMatch = block.match(/^(\w+)/);
                    currentLanguage = langMatch ? langMatch[1] : '';
                    const filename = currentLanguage ? `file.${currentLanguage}` : 'file.txt';
                    formattedCode += `\n### File: ${filename}\n\n\`\`\`${currentLanguage}\n`;
                }
                
                // Add the code content
                const codeContent = block.replace(/^(\w+)/, '').trim();
                formattedCode += codeContent + '\n```\n';
                
                inCodeBlock = true;
            } else {
                // This should be non-code text between blocks
                inCodeBlock = false;
                
                // Check if this block contains another code block
                for (const pattern of filePatterns) {
                    if (pattern.regex.test('```' + block)) {
                        formattedCode += `\n### File: ${pattern.filename}\n\n\`\`\`${pattern.language}\n`;
                        const codeContent = block.replace(/^(\w+)/, '').trim();
                        formattedCode += codeContent + '\n```\n';
                        inCodeBlock = true;
                        break;
                    }
                }
                
                if (!inCodeBlock && block.trim()) {
                    // This is explanatory text
                    formattedCode += '\n' + block.trim() + '\n';
                }
            }
        });
        
        return formattedCode || codeString;
    }
    
    // Generate code
    generateBtn.addEventListener('click', async () => {
        const prompt = promptInput.value.trim();
        
        if (!prompt) {
            alert('Please enter a prompt');
            return;
        }
        
        // Show loading state
        loadingElement.classList.remove('hidden');
        resultsElement.classList.add('hidden');
        
        try {
            const response = await fetch('/api/generate-full', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt }),
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Display results
                planOutput.textContent = data.data.plan;
                codeOutput.textContent = data.data.code;
                debugOutput.innerHTML = markdownToHtml(data.data.debug_output);
                debugPlanOutput.innerHTML = markdownToHtml(data.data.debug_plan);
                validationOutput.innerHTML = markdownToHtml(data.data.validation);
                
                // Process and display complete code with file names
                completeCodeOutput.innerHTML = markdownToHtml(processCompleteCode(data.data.code));
                
                // Highlight code
                hljs.highlightAll();
                
                // Hide loading and show results with animation
                loadingElement.classList.add('hidden');
                resultsElement.classList.remove('hidden');
                
                // Scroll to results
                resultsElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
            } else {
                throw new Error(data.message || 'An error occurred');
            }
        } catch (error) {
            alert(`Error: ${error.message}`);
            loadingElement.classList.add('hidden');
        }
    });
    
    // Clear results with animation
    clearBtn.addEventListener('click', () => {
        // Fade out results
        if (!resultsElement.classList.contains('hidden')) {
            resultsElement.style.opacity = '0';
            setTimeout(() => {
                promptInput.value = '';
                planOutput.textContent = '';
                codeOutput.textContent = '';
                debugOutput.innerHTML = '';
                debugPlanOutput.innerHTML = '';
                completeCodeOutput.innerHTML = '';
                validationOutput.innerHTML = '';
                resultsElement.classList.add('hidden');
                resultsElement.style.opacity = '1';
            }, 300);
        } else {
            promptInput.value = '';
        }
    });
    
    // Convert markdown to HTML
    function markdownToHtml(markdown) {
        if (!markdown) return '';
        
        // Simple markdown conversion
        return markdown
            .replace(/```(\w*)([\s\S]*?)```/g, (match, language, code) => {
                const escapedCode = escapeHtml(code.trim());
                const lang = language ? ` class="language-${language}"` : '';
                return `<pre><code${lang}>${escapedCode}</code></pre>`;
            })
            .replace(/`([^`]+)`/g, '<code>$1</code>')
            .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
            .replace(/\*([^*]+)\*/g, '<em>$1</em>')
            .replace(/^### (.+)$/gm, '<h3>$1</h3>')
            .replace(/\n/g, '<br>');
    }
    
    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
    
    // Add typing effect to the placeholder
    const typePlaceholder = () => {
        const placeholders = [
            "e.g., 'Build a Calculator using JavaScript'",
            "e.g., 'Create a TODO list app with React'",
            "e.g., 'Design a simple API with FastAPI'",
            "e.g., 'Make a responsive navigation menu with CSS'"
        ];
        
        let currentPlaceholder = 0;
        let charIndex = 0;
        let typingInterval;
        let currentText = '';
        let isDeleting = false;
        let pauseTime = 1000; // Time to pause at full text
        
        typingInterval = setInterval(() => {
            const placeholder = placeholders[currentPlaceholder];
            
            if (isDeleting) {
                // Deleting text
                currentText = placeholder.substring(0, charIndex--);
                promptInput.setAttribute('placeholder', currentText);
                
                // When deletion is complete, move to the next placeholder
                if (charIndex < 0) {
                    isDeleting = false;
                    currentPlaceholder = (currentPlaceholder + 1) % placeholders.length;
                    charIndex = 0;
                }
            } else {
                // Typing text
                currentText = placeholder.substring(0, charIndex++);
                promptInput.setAttribute('placeholder', currentText);
                
                // When typing is complete, pause then start deleting
                if (charIndex > placeholder.length) {
                    isDeleting = true;
                    charIndex = placeholder.length;
                    
                    // Pause before deleting
                    clearInterval(typingInterval);
                    setTimeout(() => {
                        typingInterval = setInterval(typingLoop, 50);
                    }, pauseTime);
                }
            }
        }, 50);
        
        // Create the typing loop function for reuse
        const typingLoop = () => {
            const placeholder = placeholders[currentPlaceholder];
            
            if (isDeleting) {
                currentText = placeholder.substring(0, charIndex--);
                promptInput.setAttribute('placeholder', currentText);
                
                if (charIndex < 0) {
                    isDeleting = false;
                    currentPlaceholder = (currentPlaceholder + 1) % placeholders.length;
                    charIndex = 0;
                }
            } else {
                currentText = placeholder.substring(0, charIndex++);
                promptInput.setAttribute('placeholder', currentText);
                
                if (charIndex > placeholder.length) {
                    isDeleting = true;
                    charIndex = placeholder.length;
                    
                    clearInterval(typingInterval);
                    setTimeout(() => {
                        typingInterval = setInterval(typingLoop, 50);
                    }, pauseTime);
                }
            }
        };
    };
    
    // Start the typing effect
    typePlaceholder();
    
    // Add event listener to stop the typing effect when the input is focused
    promptInput.addEventListener('focus', () => {
        promptInput.setAttribute('placeholder', '');
    });
    
    // Resume typing effect when the input loses focus (if empty)
    promptInput.addEventListener('blur', () => {
        if (!promptInput.value) {
            typePlaceholder();
        }
    });
    
    // Add keyboard shortcut - Ctrl+Enter to generate
    promptInput.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            generateBtn.click();
            e.preventDefault();
        }
    });
    
    // Add animation to the page on load
    document.body.classList.add('loaded');
});