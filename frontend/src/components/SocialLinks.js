import React from 'react';
import { SocialLink, GithubIcon, LinkedinIcon, LeetcodeIcon, CodeforcesIcon, KaggleIcon } from './SocialIcons';

const socialIcons = [   // Links to be rendered in order 
  { key: 'github', icon: GithubIcon },
  { key: 'linkedin', icon: LinkedinIcon },
  { key: 'leetcode', icon: LeetcodeIcon },
  { key: 'linkedin', icon: CodeforcesIcon },
  { key: 'linkedin', icon: KaggleIcon }
];

const SocialLinks = ({ personalInfo, size = 6, className = "" }) => {
  if (!personalInfo) return null;

  const renderSocialIcon = ({ key, icon: Icon, darkMode }) => {
    const url = personalInfo[key];
    if (!url) return null;

    return (
      <SocialLink key={key} href={url}>
        <Icon size={size} darkMode={darkMode} />
      </SocialLink>
    );
  };

  return (
    <div className={`flex space-x-4 ${className}`}>
      {socialIcons.map(({ key, icon }) => {
        if (key === 'leetcode') { // Special handling for LeetCode dark mode
          if (!personalInfo.leetcode) return null;
          return (
            <React.Fragment key={key}>
              <div className="hidden dark:block">
                {renderSocialIcon({ key, icon, darkMode: true })}
              </div>
              <div className="dark:hidden">
                {renderSocialIcon({ key, icon, darkMode: false })}
              </div>
            </React.Fragment>
          );
        }
        return (
          <React.Fragment key={key}>
            {personalInfo[key] && renderSocialIcon({ key, icon })}
          </React.Fragment>
        );
      })}
    </div>
  );
};

export default SocialLinks;
