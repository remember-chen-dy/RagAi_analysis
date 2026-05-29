import re
from typing import List, Set
from collections import Counter
from llama_index.core import Document


class HeaderFooterFilter:

    def __init__(self):
        self.common_patterns = [
            r'^第\s*\d+\s*页\s*(共\s*\d+\s*页)?$',
            r'^\d+\s*/\s*\d+$',
            r'^-\s*\d+\s*-$',
            r'^\|\s*\d+\s*\|$',
            r'^©?\s*(?:Copyright|版权所有).*?(?:\d{4})?',
            r'^(?:保养手册 v1.0 2025.01|保养手册 v1.0 2025.01|在线技术支持|Internal|Confidential|DjlMatrice 4系列保养手册)',
            r'^(?:© 2025 大疆创新 版权所有|微信扫一扫关注|大疆行业应用服务公众号|2025大疆创新 版权所有|保养手册 v1.0 2025.01):?.*$',
            r'^\w+\s+[\d\-]+\s+\w+$',
            r'^(?:www\.|http?s://)\S+',
            r'^[A-Z][a-z]+\s+\d{1,2},\s+\d{4}$',
            r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}$',
        ]

        self.max_length = 80

    def filter_by_pattern(self, text: str) -> bool:
        text = text.strip()

        if len(text) > self.max_length:
            return False

        for pattern in self.common_patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return True

        return False

    def filter_by_frequency(self, documents: List[Document], threshold: float = 0.3) -> Set[str]:
        text_counter = Counter()

        for doc in documents:
            lines = doc.text.split('\n')
            for line in lines:
                line = line.strip()
                if len(line) < self.max_length and line:
                    text_counter[line] += 1

        total_docs = len(documents)
        frequent_texts = {
            text for text, count in text_counter.items()
            if count / total_docs >= threshold
        }

        return frequent_texts

    def remove_header_footer(self, doc: Document, frequent_texts: Set[str] = None) -> str:
        lines = doc.text.split('\n')
        cleaned_lines = []

        for line in lines:
            line_clean = line.strip()

            if not line_clean:
                continue

            if self.filter_by_pattern(line_clean):
                continue

            if frequent_texts and line_clean in frequent_texts:
                continue

            cleaned_lines.append(line)

        return '\n'.join(cleaned_lines)


class AdvancedHeaderFooterFilter:

    def __init__(self):
        self.pattern_filter = HeaderFooterFilter()

    def filter_documents(self, documents: List[Document]) -> List[Document]:
        frequent_texts = self.pattern_filter.filter_by_frequency(documents, threshold=0.25)

        cleaned_documents = []
        for doc in documents:
            original_text = doc.text

            cleaned_text = self._remove_header_footer_from_text(
                original_text,
                frequent_texts
            )

            if cleaned_text.strip():
                new_doc = Document(
                    text=cleaned_text,
                    metadata=doc.metadata,
                    id_=doc.id_ if hasattr(doc, 'id_') else None
                )
                cleaned_documents.append(new_doc)

        return cleaned_documents

    def _remove_header_footer_from_text(self, text: str, frequent_texts: Set[str]) -> str:
        lines = text.split('\n')

        if len(lines) < 10:
            return text

        header_candidate_lines = lines[:3]
        footer_candidate_lines = lines[-3:]

        header_end_index = 0
        for i, line in enumerate(header_candidate_lines):
            line_clean = line.strip()
            if self._is_header_footer(line_clean, frequent_texts):
                header_end_index = i + 1
            else:
                break

        footer_start_index = len(lines)
        for i, line in enumerate(reversed(footer_candidate_lines)):
            line_clean = line.strip()
            if self._is_header_footer(line_clean, frequent_texts):
                footer_start_index = len(lines) - i - 1
            else:
                break

        cleaned_lines = lines[header_end_index:footer_start_index]

        cleaned_lines = [
            line for line in cleaned_lines
            if not self._is_inline_header_footer(line)
        ]

        return '\n'.join(cleaned_lines)

    def _is_header_footer(self, text: str, frequent_texts: Set[str]) -> bool:
        if not text:
            return False

        if len(text) > 80:
            return False

        if text in frequent_texts:
            return True

        return self.pattern_filter.filter_by_pattern(text)

    def _is_inline_header_footer(self, line: str) -> bool:
        line_lower = line.lower()

        keywords = [
            'copyright', 'confidential', 'internal', 'company name',
            '版权所有', '机密', '内部资料', '页码', 'page'
        ]

        for keyword in keywords:
            if keyword in line_lower:
                if len(line) < 100:
                    return True

        return False
