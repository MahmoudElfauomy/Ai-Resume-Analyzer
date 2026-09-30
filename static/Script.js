 const API_URL = "http://127.0.0.1:8000";

        async function analyzeResume() {
            const fileInput = document.getElementById('resumeFile');
            const btn = document.getElementById('submitBtn');

            if (fileInput.files.length === 0) {
                alert("الرجاء اختيار ملف أولاً!");
                return;
            }

            btn.innerText = "جاري التحليل بواسطة الذكاء الاصطناعي... ⏳";
            btn.disabled = true;

            const formData = new FormData();
            formData.append("file", fileInput.files[0]);

            try {
                const response = await fetch(`${API_URL}/analyze-resume/?user_id=1`, {
                    method: "POST",
                    body: formData
                });

                if (!response.ok) {
                    throw new Error("حدث خطأ في السيرفر");
                }

                const data = await response.json();

                document.getElementById('upload-section').style.display = 'none';

                document.getElementById('results-section').style.display = 'block';

                document.getElementById('ai-summary').innerText = data.summary || "لا يوجد ملخص متاح.";

                document.getElementById('skills-list').innerText = (data.detected_skills && data.detected_skills.length > 0)
                    ? data.detected_skills.join("، ")
                    : "لم يتم التعرف على مهارات واضحة.";

                const jobsContainer = document.getElementById('jobs-container');
                jobsContainer.innerHTML = ""; 

                if (data.recommendations && data.recommendations.length > 0) {
                    data.recommendations.forEach(job => {
                        jobsContainer.innerHTML += `
                            <div class="job-item">
                                <strong style="font-size: 18px;">${job.job_title} (${job.company})</strong><br>
                                <span style="color: #059669; font-weight: bold;">نسبة التوافق: ${job.match_score}</span><br>
                                <small style="color: #ef4444;">المهارات الناقصة: ${job.missing_skills.join("، ") || 'لا يوجد'}</small>
                            </div>
                        `;
                    });
                } else {
                    jobsContainer.innerHTML = "<p style='color: #64748b;'>لم يتم إضافة وظائف في قاعدة البيانات للمطابقة.</p>";
                }

            } catch (err) {
                alert("حدث خطأ! تأكد أن سيرفر البايثون يعمل.");
                console.error(err);
                btn.innerText = "تحليل السيرة الذاتية الآن";
                btn.disabled = false;
            }
        }