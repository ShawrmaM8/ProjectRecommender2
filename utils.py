TRANSLATIONS = {
    'en': {
        'title': 'Project Recommender',
        'select_complexity': 'Select Complexity',
        'select_scalability': 'Select Scalability',
        'select_practicality': 'Select Practicality',
        'recommend_button': 'Recommend Projects',
        'add_to_cart': 'Add to Cart',
        'development_cart': 'Development Cart',
        'remove': 'Remove',
        'download_project': 'Download Project Info',
        'download_cart': 'Download Cart',
        'view_dev_map': 'View Development Map'
        # Add more UI strings as needed
    },
    'ar': {
        'title': 'موصي المشاريع',
        'select_complexity': 'اختر التعقيد',
        'select_scalability': 'اختر القابلية للتوسع',
        'select_practicality': 'اختر العملية',
        'recommend_button': 'اقترح مشاريع',
        'add_to_cart': 'أضف إلى السلة',
        'development_cart': 'سلة التطوير',
        'remove': 'إزالة',
        'download_project': 'تنزيل معلومات المشروع',
        'download_cart': 'تنزيل السلة',
        'view_dev_map': 'عرض خريطة التطوير'
        # Add more Arabic equivalents as needed
    }
}


def get_text(key, lang='en'):
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)  # Fallback to English or key


def generate_dev_map(project):
    complexity = project['complexity']
    time_category = 'low' if complexity <= 3 else 'medium' if complexity <= 7 else 'high'
    time_per_step = {
        'low': '1-2 hours',
        'medium': '3-5 hours',
        'high': '6+ hours'
    }[time_category]

    avg_time_per_step = (int(time_per_step.split('-')[0]) + int(time_per_step.split('-')[1])) // 2
    total_time = len(project['steps']) * avg_time_per_step

    map_prompt = f"""
Comprehensive Code Development Map for {project['name_en']}:

Tools Used: {', '.join(project['tools'])}

Stats:
- Complexity: {complexity}/10
- Scalability: {project['scalability']}/10
- Practicality: {project['practicality']}/10
- Total Projected Time: {total_time} hours (estimate)

Step-by-Step Development:
"""
    for i, step in enumerate(project['steps'], 1):
        map_prompt += f"{i}. {step} - Projected Time: {time_per_step}\n"

    map_prompt += "\nThis map is designed for precise implementation. Start with setup and iterate."
    return map_prompt