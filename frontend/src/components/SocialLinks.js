import React from 'react';
import { SocialLink, GithubIcon, LinkedinIcon, LeetcodeIcon, CodeforcesIcon, KaggleIcon } from './SocialIcons';

// Map of platform names to their corresponding icon components
const platformIcons = {
  'github': GithubIcon,
  'linkedin': LinkedinIcon,
  'leetcode': LeetcodeIcon,
  'codeforces': CodeforcesIcon,
  'kaggle': KaggleIcon,
  'twitter': null,  // Add more as needed
  'facebook': null,
  'instagram': null,
  'youtube': null,
  'website': null
};

const SocialLinks = ({ personalInfo, size = 6, className = "" }) => {
  if (!personalInfo) return null;

  // Render a single social icon
  const renderSocialIcon = (socialLink) => {
    const { platform, url, display_text: displayText } = socialLink;
    const Icon = platformIcons[platform];
    
    if (!Icon) return null; // Skip if no icon is defined for this platform

    // Special handling for LeetCode dark mode
    if (platform === 'leetcode') {
      return (
        <React.Fragment key={socialLink.id || platform}>
          <div className="hidden dark:block">
            <SocialLink href={url} title={displayText || platform}>
              <Icon size={size} darkMode={true} />
            </SocialLink>
          </div>
          <div className="dark:hidden">
            <SocialLink href={url} title={displayText || platform}>
              <Icon size={size} darkMode={false} />
            </SocialLink>
          </div>
        </React.Fragment>
      );
    }

    return (
      <SocialLink key={socialLink.id || platform} href={url} title={displayText || platform}>
        <Icon size={size} />
      </SocialLink>
    );
  };

  // Get social links from the API response
  const socialLinks = personalInfo.social_links || [];
  
  // For backward compatibility, check for legacy social links
  const legacyLinks = [];
  if (personalInfo.github) {
    legacyLinks.push({ platform: 'github', url: personalInfo.github, id: 'legacy-github' });
  }
  if (personalInfo.linkedin) {
    legacyLinks.push({ platform: 'linkedin', url: personalInfo.linkedin, id: 'legacy-linkedin' });
  }
  if (personalInfo.leetcode) {
    legacyLinks.push({ platform: 'leetcode', url: personalInfo.leetcode, id: 'legacy-leetcode' });
  }
  if (personalInfo.codeforces) {
    legacyLinks.push({ platform: 'codeforces', url: personalInfo.codeforces, id: 'legacy-codeforces' });
  }
  if (personalInfo.kaggle) {
    legacyLinks.push({ platform: 'kaggle', url: personalInfo.kaggle, id: 'legacy-kaggle' });
  }

  // Combine and filter active social links
  const allSocialLinks = [...socialLinks, ...legacyLinks]
    .filter(link => link && link.platform && link.url && platformIcons[link.platform])
    .map(link => ({
      ...link,
      // Ensure order is a number, default to 0 if not provided
      order: typeof link.order === 'number' ? link.order : 0
    }))
    // Sort by order, then by platform name for consistent ordering
    .sort((a, b) => a.order - b.order || a.platform.localeCompare(b.platform));

  return (
    <div className={`flex space-x-4 ${className}`}>
      {allSocialLinks.map(renderSocialIcon)}
    </div>
  );
};

export default SocialLinks;
